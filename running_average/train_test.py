"""An E2E test for the running average example.

The test uses a direct session as opposed to running distributed or on the
Cloud ML service.

To run the test, running_average should be a top level package. Then invoke the test.
e.g. 
  python -m running_average.train_test
"""

import datetime
import json
import logging
import os
import subprocess
import tempfile
import tensorflow as tf
import unittest

import numpy as np
from tensorflow.core.example import example_pb2

from google.cloud import dataflow as df
from google.cloud.dataflow import coders as df_coders
from google.cloud.ml.dataflow import train_with_graph_builder_transform
from google.cloud.ml.dataflow import train_with_tf_transform
from google.cloud.ml.dataflow import training_service
from google.protobuf import json_format

from running_average import data

class TrainRunningAverage(unittest.TestCase):

  def testTrainLocal(self):
    example_data = data.create_examples(100, 5)

    with tempfile.NamedTemporaryFile(delete=False) as hf:
      input_path = hf.name
      
    with tf.python_io.TFRecordWriter(input_path) as hf:
      for e in example_data:
        hf.write(e.SerializeToString())

      
    output_path = tempfile.mkdtemp(prefix='tmpRunningAverageLocal')
    logging.info('Using output path: %s', output_path)
    args = ["python", "-m", "running_average.running_average_main", "--train_data_path=" + input_path,
            "--output_path=" + output_path]

    # We invoke it as a subprocess because we want to verify command line parsing
    # doesn't have problems.
    logging.info("Running: %s", " ".join(args))
    subprocess.check_call(args)
    
    # TODO(jlewi): Add more assertions. We should check 
    #  1. The trained value.
    #  2. The exported model.


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()