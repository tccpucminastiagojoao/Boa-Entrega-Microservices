# Boa Entrega Deploy

## Develop Environment Install
* Install Docker Desktop WSL 2 backend: https://docs.docker.com/desktop/windows/wsl/
* Install VSCode: https://code.visualstudio.com/
* Open this project in VSCode
* Install Remote Development Extension Pack in VSCode
* Use the "Remote-Containers: Open Folder in Container..." command from the Command Palette (Ctrl+Shift+P)
    * Details: https://code.visualstudio.com/docs/remote/containers
* Configure GCloud in Remote Container terminal:
    * Command: gcloud init --console-only

## Boa Entrega Deploy Commands:
* create-all.sh: Create all cluster and deployments in GKE
* delete-all.sh: Delete all cluster and deployments in GKE
* create-cluster.sh: Create cluster in GKE
* delete-cluster.sh: Delete cluster in GKE
* deploy-persistence.sh: Deploy all persistences in cluster GKE
* delete-persistence.sh: Delete all persistences in cluster GKE
* deploy-services.sh: Deploy all services in cluster GKE
* delete-services.sh: Delete all services in cluster GKE

## Access services:
* Open: https://console.cloud.google.com/kubernetes/discovery?organizationId=0&project=applied-mystery-342719

## Configure jBPM Server
* Access jBPM: http://PUBLIC-IP-load-balancer-jbpm-server-full:8080/business-central/
    * Username: wbadmin
    * Password: wbadmin
* Create project Boa-Entrega in MySpace
* Import Asset Entrega-Padrao (modulo-servicos-ao-cliente/jbpm-server-full/bpm-assets/Entrega-Padrao.bpmn)
* Deploy Project Boa-Entrega
* Check process definitions in pedidos: http://PUBLIC-IP-kong-proxy/pedidos/process/definitions

## Create fake pedidos using REST API
* Command: ./modulo-servicos-ao-cliente/servico-acompanhamento-workflow/create-fake-pedidos.sh "PUBLIC-IP-kong-proxy" NUMBER_OF_PEDIDOS