#!/bin/bash

#ENDPOINT=https://cloudml-jlewi-test.sandbox.googleapis.com/v1alpha3
# Must have a trailing slash
ORIGIN=gs://cloud-ml-dev_jlewi/running_average/0627-040112/exported_model/
python -m running_average.deploy_model \
  --origin_uri=${ORIGIN} \
  --project_id=cloud-ml-dev \
  --version=v0627_040112