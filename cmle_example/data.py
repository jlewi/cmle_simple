"""This module contains routines for working with the data."""

import logging
import numpy as np
from tensorflow.core.example import example_pb2
from google.protobuf import json_format

def create_examples(num_examples, input_mean):
  """Create ExampleProto's containg data."""
  ids = np.arange(num_examples).reshape([num_examples, 1])
  inputs = np.random.randn(num_examples, 1) + input_mean
  target = inputs - input_mean
  example_data = []
  for row in range(num_examples):
    logging.info("Creating example: %s", row + 1)
    e = example_pb2.Example()
    e.features.feature['id'].bytes_list.value.append(str(ids[row, 0]))
    e.features.feature['target'].float_list.value.append(target[row, 0])
    e.features.feature['inputs'].float_list.value.append(inputs[row, 0])
    example_data.append(e)
  return example_data
