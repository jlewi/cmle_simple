#!/bin/bash
python -m running_average.create_training_data \
    --output_path=gs://dataflow-jlewi_cloud_ml/running_average/input/inputs.tfrecord