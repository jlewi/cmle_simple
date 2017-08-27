"""A program for creating training data.

This program can be used to create training data on GCS for use with testing.
"""

import argparse
import logging
import os
import subprocess
import tempfile
import tensorflow as tf

from cmle_example import data


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser(description='Generate Some Test Data.')
  parser.add_argument('--output_path',
                      help='The GCS path to which output will be written.') 
  args = parser.parse_args()

  logging.info("Creating data")
  example_data = data.create_examples(100, 5)
  logging.info("Writing to file")
  with tf.python_io.TFRecordWriter(args.output_path) as hf:
    for i, e in enumerate(example_data):
      logging.info("Appending record %s", i)
      hf.write(e.SerializeToString())
      
  logging.info("Data written to: %s", args.output_path)