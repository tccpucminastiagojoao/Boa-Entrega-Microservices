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

# Create GKE cluster
gcloud container --project "${PROJECT_ID}" clusters create "${gcloud_cluster}" --zone "${gcloud_cluster_zone}" --no-enable-basic-auth --cluster-version "1.21.6-gke.1503" --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/${PROJECT_ID}/global/networks/default" --subnetwork "projects/${PROJECT_ID}/regions/${gcloud_cluster_region}/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --enable-shielded-nodes --node-locations "${gcloud_cluster_zone}"

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