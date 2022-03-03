#!/bin/bash

export PROJECT_ID="applied-mystery-342719"
echo $PROJECT_ID
gcloud config set project $PROJECT_ID

# southamerica-east1-docker.pkg.dev/applied-mystery-342719/tccpucminastiagojoao-repo
gcloud_repo_region="southamerica-east1"
gcloud_repo_id="tccpucminastiagojoao-repo"

gcloud_cluster="tccpucminastiagojoao-cluster"
gcloud_cluster_zone="southamerica-east1-a"

# Configure gcloud docker
gcloud auth configure-docker ${gcloud_repo_region}-docker.pkg.dev
gcloud artifacts repositories list

# Get credentials to GKE cluster
gcloud container clusters get-credentials ${gcloud_cluster} --zone ${gcloud_cluster_zone} --project ${PROJECT_ID}

build_apply_microservice() {
    microservice_name="${1}"
    microservice_version="${2}"
    microservice_service="${3}"

    microservice_tag="${gcloud_repo_region}-docker.pkg.dev/${PROJECT_ID}/${gcloud_repo_id}/${microservice_name}:${microservice_version}"

    # Build and send to gcloud_repo_id
    # docker image rm -f ${microservice_tag}
    docker build ./${microservice_name}/ -t ${microservice_tag}
    docker push ${microservice_tag}

    kubectl delete -f ./${microservice_name}/deployment-gcloud.yaml
    kubectl apply -f ./${microservice_name}/deployment-gcloud.yaml
}

# Apply server jbpm-server-full
SERVER_NAME=jbpm-server-full
SERVER_VERSION=0.0.1
SERVER_NODE_PORT=node-port-${SERVER_NAME}

#kubectl delete -f ./${SERVER_NAME}/deployment.yaml
kubectl apply -f ./${SERVER_NAME}/deployment.yaml
