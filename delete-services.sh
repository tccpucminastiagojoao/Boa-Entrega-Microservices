#!/bin/bash

# Cluster definitions
source cluster-definitions.sh

# Get credentials to GKE cluster
gcloud container clusters get-credentials ${gcloud_cluster} --zone ${gcloud_cluster_zone} --project ${PROJECT_ID}

delete_microservice() {
    module_name="${1}"
    service_name="${2}"

    # Delete microservice
    kubectl delete -f ./${module_name}/${service_name}/deployment.yaml
}

# Delete microservices
delete_microservice "modulo-informacoes-cadastrais" "servico-informacoes-de-clientes"
delete_microservice "modulo-informacoes-cadastrais" "servico-informacoes-de-destinatarios"
delete_microservice "modulo-servicos-ao-cliente" "servico-acompanhamento-workflow"
delete_microservice "modulo-gestao-estrategica" "servico-acompanhamento-indicadores"

# Delete server jbpm-server-full
MODULE_NAME="modulo-servicos-ao-cliente"
SERVER_NAME="jbpm-server-full"
kubectl delete -f ./${MODULE_NAME}/${SERVER_NAME}/deployment.yaml

# Delete Kong for Kubernetes
kubectl delete -f https://bit.ly/k4k8s

# Delete ingresses for microservices
kubectl delete -f deployment-ingress.yaml
