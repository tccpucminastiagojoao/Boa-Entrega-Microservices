#!/bin/bash

# Cluster definitions
source cluster-definitions.sh

# Configure gcloud docker
gcloud auth configure-docker ${gcloud_repo_region}-docker.pkg.dev

# Get credentials to GKE cluster
gcloud container clusters get-credentials ${gcloud_cluster} --zone ${gcloud_cluster_zone} --project ${PROJECT_ID}

build_apply_microservice() {
    module_name="${1}"
    service_name="${2}"
    microservice_name="${3}"
    microservice_version="${4}"

    microservice_tag="${gcloud_repo_region}-docker.pkg.dev/${PROJECT_ID}/${gcloud_repo_id}/${microservice_name}:${microservice_version}"

    # Build and send to gcloud_repo_id
    # docker image rm -f ${microservice_tag}
    docker build ./${module_name}/${service_name}/ -t ${microservice_tag}
    docker push ${microservice_tag}

    # Apply microservice
    kubectl apply -f ./${module_name}/${service_name}/deployment.yaml
}

# Apply server jbpm-server-full
MODULE_NAME="modulo-servicos-ao-cliente"
SERVER_NAME="jbpm-server-full"
kubectl apply -f ./${MODULE_NAME}/${SERVER_NAME}/deployment.yaml

# Apply microservices
build_apply_microservice "modulo-informacoes-cadastrais" "servico-informacoes-de-clientes" "mic-sic-microservice" "0.0.1"
build_apply_microservice "modulo-informacoes-cadastrais" "servico-informacoes-de-destinatarios" "mic-sid-microservice" "0.0.1"
build_apply_microservice "modulo-servicos-ao-cliente" "servico-acompanhamento-workflow" "msc-saw-microservice" "0.0.1"
build_apply_microservice "modulo-gestao-estrategica" "servico-acompanhamento-indicadores" "mge-sai-microservice" "0.0.1"

# Install Kong for Kubernetes
kubectl create -f https://bit.ly/k4k8s

# Define ingresses for microservices
kubectl apply -f deployment-ingress.yaml
