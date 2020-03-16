import os
import uuid
import time
import logging
import datetime
import requests
import traceback
from pathlib import Path
from copy import deepcopy
from multiprocessing import Process


import pykube

from config import *


logging.basicConfig(level=logging.INFO)

fileN = 0
jobsNum = 200
config_k8s = pykube.KubeConfig.from_url(K8S_PROXY)
api = pykube.HTTPClient(config_k8s)
api.timeout = 1e6


def status_checker(job) -> str:
    active = job.obj['status'].get('active', 0)
    succeeded = job.obj['status'].get('succeeded', 0)
    failed = job.obj['status'].get('failed', 0)
    if succeeded:
        return 'succeeded'
    elif active:
        return 'wait'
    elif failed:
        return 'failed'
    return 'wait'

def get_experiment_folder() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def job_status(jobs_status):
    if 'failed' in jobs_status:
        return 'failed'
    elif all([status == 'succeeded' for status in jobs_status]):
        return 'exited'
    return 'wait'


def to_kube_env(envs) -> list:
    kube_env = []
    for k, v in envs.items():
        kube_env.append({"name": str(k), "value": str(v)})
    return kube_env


def run_kube_job(job_spec: dict,
                 envs: dict,
                 job_folder: str,
                 timeout: int) -> str:
    job_tag = "-".join(job_folder.split("/")[-2:])
    job_uuid: str = f"ek-{str(uuid.uuid4())[:5]}-{job_tag}"
    job_spec["metadata"]["name"] = job_spec["metadata"]["name"].format(job_uuid)

    job_spec["spec"]["template"]["spec"]["volumes"][0]["hostPath"]["path"] = job_folder

    job_spec["spec"]["template"]["spec"]["containers"][0]["env"] = to_kube_env(envs)


    job = pykube.Job(api, job_spec)
    job.create()
    start = datetime.datetime.now()
    status = "start"
    logging.info(f"JOB: {job_uuid} was started. Tag is {job_tag}")
    while (datetime.datetime.now() - start).seconds < timeout:
        try:
            time.sleep(10)
            job.reload()
            status = status_checker(job=job)
            if status == "succeeded":
                logging.info(f"JOB: {job_uuid} finished. Output in {job_folder}")
                job.delete("Foreground")
                return status
        except requests.exceptions.HTTPError as exc:
            print(f"{exc} {traceback.print_exc()}")
    print(f"Timeout {timeout} was exceeded. Deleting the job {job_uuid}")
    job.delete("Foreground")
    return status


fileLen = {0: 13450391, 16000: 6242698, 66000: 6112412, 27000: 6238416,
           63000: 6242811, 21000: 6236055, 34000: 6241933, 57000: 6240829,
           10000: 6237695, 23000: 6234706, 26000: 6241631, 15000: 6245846,
           60000: 6239611, 58000: 6235854, 29000: 6237372, 31000: 6238463,
           39000: 6244654, 4000: 6237671, 22000: 2110646, 44000: 2793980,
           59000: 6235770, 9000: 6239653, 47000: 6236843, 36000: 6239944,
           14000: 6239735, 5000: 6238535, 45000: 6238019, 51000: 6242407,
           41000: 6240065, 19000: 6234737, 49000: 6238063, 55000: 6240257,
           33000: 6240302, 8000: 6239151, 20000: 6238057, 25000: 6236993,
           61000: 6236622, 13000: 6244139, 38000: 6239812, 52000: 6243558,
           30000: 6238488, 2000: 6238126, 3000: 6239983, 43000: 6239453,
           28000: 6234302, 7000: 6246430, 53000: 6237809, 35000: 6238593,
           56000: 6239181, 12000: 6239670, 18000: 6242505, 48000: 6238654,
           54000: 6240632, 1000: 6240925, 62000: 3702269, 42000: 6242558,
           64000: 6239932, 32000: 3881168, 6000: 6242602, 17000: 6243827,
           40000: 6237918, 24000: 6238708, 50000: 5520395, 11000: 6238705,
           65000: 6239301, 37000: 6238285, 46000: 6240834}

procs = []

nEvents_in = fileLen[fileN * 1000]
# nEvents_in = 100
n = nEvents_in
k = jobsNum
baseName = "baseMaster"
startPoints = [i * (n // k) + min(i, n % k) for i in range(k)]
chunkLength = [(n // k) + (1 if i < (n % k) else 0) for i in range(k)]
chunkLength[-1] = chunkLength[-1] - 1
exp_folder = get_experiment_folder()

for i in range(200):
    job_folder = str(Path(HOST_OUTPUT_DIRECTORY) / exp_folder / baseName / str(fileN) / str(i))
    os.makedirs(job_folder)
    logging.info(f"Job folder {job_folder} is created")
    envs = {"fileName": fileN, #"pythia8_Geant4_10.0_withCharmandBeauty0_mu.root",
            "mfirstEvent": startPoints[i],
            "nEvents": chunkLength[i],
            "muShieldDesign": 9,
            "jName": "baseName",
            "jNumber": i + 1}
    job_spec = deepcopy(JOB_SPEC)
    proc = Process(target=run_kube_job, args=(job_spec,
                                              envs,
                                              job_folder,
                                              TIMEOUT))
    procs.append(proc)
    proc.start()
for proc in procs:
    proc.join()
