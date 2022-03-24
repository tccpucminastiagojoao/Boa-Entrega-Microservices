#!/bin/bash

# Cluster definitions
source cluster-definitions.sh

# Delete GKE cluster
gcloud container clusters delete ${gcloud_cluster} --zone ${gcloud_cluster_zone}
