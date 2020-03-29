#!/usr/bin/env python
# -*- coding: utf-8 -*-

# parameters of server
K8S_PROXY = 'http://127.0.0.1:8002'

HOST_OUTPUT_DIRECTORY = 'data/EK_output'
HOST_LOCALOUTPUT_DIRECTORY = '/mnt/shipfs/EK_output'
DOCKER_OUTPUT_DIRECTORY = '/output'

# HOST_SAMPLE_DIRECTORY - local folder in the cluster
HOST_SAMPLE_DIRECTORY = '/local/ship/background_2018'
DOCKER_SAMPLE_DIRECTORY = '/sample'

TIMEOUT = 60*60*7


JOB_SPEC = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        # Fill in the python script
        "name": "{}"
    },
    "spec": {
        # Don't forget about this disabled option
        # "ttlSecondsAfterFinished": 14400,
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "ekship",
                        "image": "mrphys/mfsimage:azcpy_fs_master_2",
                        # Set env in the code
                        # "env": [
                        #     {"name": "fileName",
                        #      "value": "pythia8_Geant4_10.0_withCharmandBeauty0_mu.root"},
                        #     {"name": "mfirstEvent",
                        #      "value": "0"},
                        #     {"name": "nEvents",
                        #      "value": "10"},
                        #     {"name": "muShieldDesign",
                        #      "value": "9"},
                        #     {"name": "jName",
                        #      "value": "testJob"},
                        #     {"name": "jNumber",
                        #      "value": "1"},
                        # ],
                        "resources": {
                            "requests": {
                                "memory": "6Gi",
                                "cpu": "1"
                            },
                            "limits": {
                                "memory": "6Gi",
                                "cpu": "1"
                            }
                        },
                        "volumeMounts": [
                            {
                                "mountPath": DOCKER_OUTPUT_DIRECTORY,
                                "name": "output"
                            },
                            {
                                "mountPath": DOCKER_SAMPLE_DIRECTORY,
                                "name": "muonsample",
                                "readOnly": True,
                            }
                        ]
                    }
                ],
                "hostNetwork": True,
                "restartPolicy": "Never",
                "volumes": [
                    # Use this with mount
                    # {
                    #     "name": "output",
                    #     "hostPath": {
                    #         # Fill in the python script
                    #         "path": "",
                    #         "type": "Directory"
                    #     }
                    # },
                    # Use this with azcopy
                    {
                        "name": "output",
                        "emptyDir": {}
                    },
                    {
                        "name": "muonsample",
                        "hostPath": {
                            "path": HOST_SAMPLE_DIRECTORY,
                            "type": "Directory"
                        }
                    }
                ]
            }
        },
        "backoffLimit": 1
    }
}
