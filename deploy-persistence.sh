#!/bin/bash

# Cluster definitions
source cluster-definitions.sh

# Get credentials to GKE cluster
gcloud container clusters get-credentials ${gcloud_cluster} --zone ${gcloud_cluster_zone} --project ${PROJECT_ID}

apply_microservice_persistence() {
    module_name="${1}"
    service_name="${2}"

    # Apply microservice persistence
    kubectl apply -f ./${module_name}/${service_name}/deployment-persistence.yaml
}

# Apply server persistence jbpm-server-full
MODULE_NAME=modulo-servicos-ao-cliente
SERVER_NAME=jbpm-server-full
SERVER_VERSION=0.0.1
SERVER_NODE_PORT=node-port-${SERVER_NAME}
kubectl apply -f ./${MODULE_NAME}/${SERVER_NAME}/deployment-persistence.yaml

# Apply microservices persistences
apply_microservice_persistence "modulo-informacoes-cadastrais" "servico-informacoes-de-clientes"
apply_microservice_persistence "modulo-informacoes-cadastrais" "servico-informacoes-de-destinatarios"
apply_microservice_persistence "modulo-servicos-ao-cliente" "servico-acompanhamento-workflow"
apply_microservice_persistence "modulo-gestao-estrategica" "servico-acompanhamento-indicadores"