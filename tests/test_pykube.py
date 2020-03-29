import pykube
import requests
import traceback
import time
import sys


K8S_PROXY = 'http://127.0.0.1:8002'
config_k8s = pykube.KubeConfig.from_url(K8S_PROXY)
api = pykube.HTTPClient(config_k8s)
JOB_SPEC = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        # Fill in the python script
        "name": "testjob"
    },
    "spec": {
        # Don't forget about this disabled option
        # "ttlSecondsAfterFinished": 14400,
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "testjob",
                        "image": "busybox",
                    }
                ],
                "hostNetwork": True,
                "restartPolicy": "Never",
            }
        },
        "backoffLimit": 1
    }
}


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

def job_wait(job):
    while True:
        try:
            time.sleep(10)
            job.reload()
            status = status_checker(job=job)
            if status == "succeeded":
                job.delete("Foreground")
                return status
        except requests.exceptions.HTTPError as exc:
            print(f"{exc} {traceback.print_exc()}")

def test_job_create():
    job = pykube.Job(api, JOB_SPEC)
    job.create()
    status = job_wait(job)
    job.delete()



test_job_create()