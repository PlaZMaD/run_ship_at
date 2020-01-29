# run_kubernetes
You have to make sure that there is mounted Azure File Storage on the
 machine you are runnning this code.
 
1. `df -h` to check mounted AFS
2. AFS has to be mounted to the /mnt/shipfs folder and have enough space
3. Make sure yout `config.py` is correct:

    `K8S_PROXY` - check if you do not have a 
    connection to kubernetes (`kubectl get jobs`)
    
    `HOST_OUTPUT_DIRECTORY` - set the output folder for your experiments
    
    `DOCKER_OUTPUT_DIRECTORY`, `DOCKER_SAMPLE_DIRECTORY` - set these parameters 
    according to your docker image
    
    `TIMEOUT` - set your timeout for every Job
    
    `JOB_SPEC` - check this
    
4. Launch - `python run_kubernetes.py`
5. Monitor your Jobs with `kubectl` utility:    
    pod_name = job_name - random[:5]
    
        
    kubectl --server=127.0.0.1:8002 get jobs      
    kubectl --server=127.0.0.1:8002 get pods    
    kubectl --server=127.0.0.1:8002 describe pod <pod_name>    
    kubectl --server=127.0.0.1:8002 logs <pod_name>

# run_ship_at
scripts to run fs
