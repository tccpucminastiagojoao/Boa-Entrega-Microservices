#!/bin/bash

# Cluster definitions
source cluster-definitions.sh

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
delete_microservice_persistence "modulo-gestao-estrategica" "servico-acompanhamento-indicadores"

# Delete server jbpm-server-full persistence
MODULE_NAME="modulo-servicos-ao-cliente"
SERVER_NAME="jbpm-server-full"
kubectl delete -f ./${MODULE_NAME}/${SERVER_NAME}/deployment-persistence.yaml
