#!/bin/bash

export PROJECT_ID="applied-mystery-342719"
gcloud config set project $PROJECT_ID

# southamerica-east1-docker.pkg.dev/applied-mystery-342719/tccpucminastiagojoao-repo
gcloud_repo_region="southamerica-east1"
gcloud_repo_id="tccpucminastiagojoao-repo"

gcloud_cluster="tccpucminastiagojoao-cluster"
gcloud_cluster_region="southamerica-east1"
gcloud_cluster_zone="southamerica-east1-a"
