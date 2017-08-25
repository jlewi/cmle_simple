#!/bin/bash
ENDPOINT=https://cloudml-jlewi-test.sandbox.googleapis.com/v1alpha3
#ENDPOINT=""https://cloudml-jlewi-test.sandbox.googleapis.com/v1alpha3""
python -m running_average.online_predict \
  --project_id=cloud-ml-dev \
  --model=running_average \
  --version=v0627_040112