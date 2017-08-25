#!/bin/bash
# Run training locally but using GCS input and output.
set -e

DATESTAMP=`TZ='America/Los_Angeles' date +%m%d-%H%M%S`
OUTPUT=gs://cloud-ml-dev_jlewi/running_average/${DATESTAMP}
export PATH=/opt/google/google-cloud-sdk/bin/:$PATH 

INPUT=gs://cloud-ml-dev_jlewi/running_average/input/inputs.tfrecord
#INPUT=/tmp/inputs.tfrecord
python -m running_average.running_average_main \
  --train_data_path=${INPUT} \
  --output_path=${OUTPUT}