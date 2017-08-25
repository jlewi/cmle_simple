"""A program for creating training data.

This program can be used to create training data on GCS for use with testing.
"""

import argparse
import logging
import os
import subprocess
import tempfile
import tensorflow as tf

from running_average import data


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser(description='Generate Some Test Data.')
  parser.add_argument('--output_path',
                      help='The GCS path to which output will be written.') 
  args = parser.parse_args()

  example_data = data.create_examples(100, 5)
  with tf.python_io.TFRecordWriter(args.output_path) as hf:
    for e in example_data:
      hf.write(e.SerializeToString())
      
  logging.info("Data written to: %s", args.output_path)