"""An E2E test for the running average example.

The test uses a direct session as opposed to running distributed or on the
Cloud ML service.

To run the test, running_average should be a top level package. Then invoke the test.
e.g. 
  python -m running_average.train_test
"""

import logging
import os
import subprocess
import tempfile
import tensorflow as tf
import unittest

from cmle_example import data
from cmle_example import build_saved_model

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
    train_path = os.path.join(output_path, "train_output")
    args = ["python", "-m", "cmle_example.train", "--train_data_path=" + input_path,
            "--output_path=" + train_path]

    # We invoke it as a subprocess train_path we want to verify command line parsing
    # doesn't have problems.
    logging.info("Running: %s", " ".join(args))
    subprocess.check_call(args)

    save_path = os.path.join(output_path, 'savd_model')
    build_saved_model.save_model(train_path, save_path)
    # TODO(jlewi): Add more assertions. We should check 
    #  1. The trained value.
    #  2. The exported model.


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  unittest.main()