# TCC-POC3

## GCloud

### Instalar Shell
* https://cloud.google.com/sdk/docs/install#deb

### Deploy Kubernetes

* https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app#cloud-shell

### Create Docker repository

> Console (tccpucminastiagojoao-repo - southamerica-east1):  
> https://console.cloud.google.com/artifacts/create-repo?project=applied-mystery-342719

#### Create cluster Kubernetes

> Shell (tccpucminastiagojoao-cluster - southamerica-east1-a):  
> gcloud beta container --project "applied-mystery-342719" clusters create "tccpucminastiagojoao-cluster" --zone "southamerica-east1-a" --no-enable-basic-auth --cluster-version "1.21.6-gke.1503" --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/applied-mystery-342719/global/networks/default" --subnetwork "projects/applied-mystery-342719/regions/southamerica-east1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --enable-shielded-nodes --node-locations "southamerica-east1-a"

#### Delete cluster Kubernetes:

> Shell:  
> gcloud container clusters delete "tccpucminastiagojoao-cluster" --zone "southamerica-east1-a"

## Tricks:

### Access bash in running Pod

* kubectl get pod
* kubectl exec --stdin --tty pod-name -- /bin/bash

### Access jBPM business-central
* Port forward: kubectl port-forward jbpm-server-full :8080
* Path: /business-central