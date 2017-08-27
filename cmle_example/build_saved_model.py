"""Build a saved model suitable for serving a simple model.

The model implements the equations
y = x - w
w is trained as a mean of the input.
This means w only depends on the most recent batch of training data.
"""
import argparse
import collections
import datetime
import glob
import json
import logging
import os
import tempfile
import time

import numpy as np
import tensorflow as tf

from tensorflow.contrib.session_bundle import exporter

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import signature_def_utils
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model import utils as saved_model_utils


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--checkpoint_path",
        required=True,
        help="Directory where the model checkpoint was stored.")

    parser.add_argument(
        "--save_path",
        required=True,
        help="Directory where the saved model should be stored.")


    # TODO(jlewi): We ignore unknown arguments because the backend is currently
    # setting some flags to empty values like metadata path.
    args, _ = parser.parse_known_args()
    return args


def save_model(checkpoint_path, save_path):
    """Export the trained model for serving.

    Args:
      checkpoint_path: The path where the checkpoints were saved.
      output_path: The directory where the model should be exported.
    """
    # We build a different graph for serving. We do this because we don't want the reader ops and others
    # used for serving.
    logging.info("Exporting the model to %s", save_path)

    # Build the graph
    with tf.Graph().as_default() as inference_graph:
        with tf.name_scope('inputs'):
            # The input is a string containing a serialized Example proto.
            input_data = tf.placeholder(tf.string, name='inputs')

        features = tf.parse_example(
            input_data,
            features={
                'inputs': tf.FixedLenFeature(shape=[], dtype=tf.float32, default_value=[-1]),
            })

        inputs = features['inputs']

        # The initial value should be such that type is correctly inferred as
        # float.
        weights = tf.Variable([0.0], name='weights')
        outputs = tf.add(inputs, tf.negative(weights))

        # Restore the variables from the checkpoint
        checkpoint = tf.train.latest_checkpoint(checkpoint_path)
        logging.info("Restoring weights from: %s", checkpoint)
        with tf.Session() as sess:
            saver = tf.train.Saver()
            saver.restore(sess, checkpoint)

            ### DEFINE SAVED MODEL SIGNATURE

            logging.info("inputs: %s", inputs.name)
            inputs = {'inputs': tf.saved_model.utils.build_tensor_info(inputs)}

            outputs = {'outputs': tf.saved_model.utils.build_tensor_info(outputs)}

            signature = tf.saved_model.signature_def_utils.build_signature_def(
                inputs=inputs,
                outputs=outputs,
                method_name='tensorflow/serving/predict'
            )

            ### SAVE OUT THE MODEL

            b = saved_model_builder.SavedModelBuilder(save_path)
            b.add_meta_graph_and_variables(sess,
                                           [tf.saved_model.tag_constants.SERVING],
                                           signature_def_map={'serving_default': signature})
            b.save()


def main(args):
    """Run training

    Args:
      args: Object containing the command line arguments.
    """
    save_model(args.checkpoint_path, args.save_path)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    args = parse_args()
    main(args)
