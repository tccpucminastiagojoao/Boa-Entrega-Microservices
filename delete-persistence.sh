#!/bin/bash

export PROJECT_ID="applied-mystery-342719"
echo $PROJECT_ID
gcloud config set project $PROJECT_ID

# southamerica-east1-docker.pkg.dev/applied-mystery-342719/tccpucminastiagojoao-repo
gcloud_repo_region="southamerica-east1"
gcloud_repo_id="tccpucminastiagojoao-repo"

gcloud_cluster="tccpucminastiagojoao-cluster"
gcloud_cluster_region="southamerica-east1"
gcloud_cluster_zone="southamerica-east1-a"

# Configure gcloud docker
gcloud auth configure-docker ${gcloud_repo_region}-docker.pkg.dev

# Get credentials to GKE cluster
gcloud container clusters get-credentials ${gcloud_cluster} --zone ${gcloud_cluster_zone} --project ${PROJECT_ID}

delete_microservice_persistence() {
    module_name="${1}"
    service_name="${2}"

    # Delete microservice persistence
    kubectl delete -f ./${module_name}/${service_name}/deployment-persistence.yaml
}

# Delete microservices persistences
delete_microservice_persistence "modulo-informacoes-cadastrais" "servico-informacoes-de-clientes"
delete_microservice_persistence "modulo-informacoes-cadastrais" "servico-informacoes-de-destinatarios"
delete_microservice_persistence "modulo-servicos-ao-cliente" "servico-acompanhamento-workflow"

# Delete server jbpm-server-full persistence
MODULE_NAME="modulo-servicos-ao-cliente"
SERVER_NAME="jbpm-server-full"
kubectl delete -f ./${MODULE_NAME}/${SERVER_NAME}/deployment-persistence.yaml
