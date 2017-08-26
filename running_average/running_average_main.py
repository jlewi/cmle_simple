"""Train a simple model.

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
    "--train_data_path",
    action="append",
    dest="train_data_paths",
    required=True,
    help="Directory where the output should be stored")
    
  parser.add_argument(
    "--output_path",
    required=True,
    help="Directory where the output should be stored")
    
  #******************************************************************************
  # args required by Cloud ML
  parser.add_argument(
    "--cluster_spec",
    default=None,
    help=("Json representation of the cluster specification. This will be set by "
          "the Cloud ML service."))
  parser.add_argument(
    "--job_name", 
    default=None,
    help=("This will be set by the Cloud ML service to 'ps' or "
          "worker' depending on what role the process plays in "
          "the cluster."))
  parser.add_argument(
    "--task_index",
    default=None,
    type=int,
    help=("The task index for the process. This will be set "
          "by the service."))


  # TODO(jlewi): We ignore unknown arguments because the backend is currently
  # setting some flags to empty values like metadata path.
  args, _ = parser.parse_known_args()
  return args


def run(server, train_data_paths, output_path, is_chief):
  """ Build the graph, train the model and export for inference.

  Args:
    server: Server object. Only needs to be provided if running in distributed
      mode. Should be None if running in a DirectSession.
    train_data_paths: List of the files containing the training data. These should be
      TFRecord files of Example protos.
  """

  # construct the graph and create a saver object
  with tf.Graph().as_default() as g:
    graph_ops = build_graph(train_data_paths)

    # TODO(jlewi): We moved the saver into _train_model
    saver = tf.train.Saver(tf.all_variables())

    # Create a summary writer
    summary_location = os.path.join(output_path, "summaries")
    logging.info("Writing summaries to: %s", summary_location)
    summary_writer = tf.summary.FileWriter(
        summary_location,
        graph=g)
  
    save_dir = os.path.join(output_path, "save_dir")
    logging.info("Save directory: %s", save_dir)
    if is_chief:
      saver = tf.train.Saver()
    else:
      saver = None
  
    init_op = tf.group(tf.initialize_all_variables())
  
    # Create a "supervisor", which oversees the training process.
    sv = tf.train.Supervisor(
        is_chief=is_chief,
        logdir=save_dir,
        init_op=init_op,
        # TODO(jlewi): Add a summary op?
        # summary_op=summary_op,
        saver=saver,
        global_step=graph_ops.global_step,
        save_model_secs=600)
  
    # The supervisor takes care of session initialization and restoring from
    # a checkpoint.
    if server:
      target = server.target
    else:
      # Create a direct session.
      target = ""
  
    logging.info("Server target: %s", target)
    with sv.managed_session(target) as sess:
      # Start queue runners for the input pipelines (if any).
      sv.start_queue_runners(sess)
  
      step = 0
      # Loop until we run out of training data. When the input_producer runs
      # out of data we will raise an OutOfRangeErrorr
      try:
        while not sv.should_stop():
          start_time = time.time()
          # Run one step of the model.
          sess.run(graph_ops.train)
          duration = time.time() - start_time
          if step % 100 == 0:
            # Status logging.
            logging.info("Step %d: Time %d: Time-per-step %d", step, start_time,
                         1000 * duration)
          step += 1
      except tf.errors.OutOfRangeError:
        # An OutOfRangeError indicates that we have finished processing all
        # the data so we are done.
        logging.info("Done training for %d steps.", step)
      finally:
        logging.info("Training completed.")
        if is_chief:
          logging.info("Save final checkpoint.")
          saver.save(sess, save_dir, global_step=step)
          

        logging.info("Stopping services.")
        # Ask for all the services to stop.
        # TODO(jlewi): Should we be calling stop on all workers or just the chief?
        sv.stop()
        
        logging.info("Services stopped.")


GraphOps = collections.namedtuple(
    'GraphOps', ['weights', 'global_step', 'train', 'inputs', 'targets'])

def build_graph(train_data_paths):
  """Build the graph.
  
  Tensorflow ops are added to the default graph.
  """
  
  # TODO(jlewi): We probably want to shuffle this so each worker would get different data.
  # We set num_epochs to 1 so we only do a single pass over the data before raising an out of range
  # error.
  filename_queue = tf.train.string_input_producer(train_data_paths, num_epochs=1)
  
  reader = tf.TFRecordReader()
  _, serialized_example = reader.read(filename_queue)
  # TODO(jlewi): What are sensible values?
  batch_size = 20
  capacity = 20
  MIN_AFTER_DEQUEUE = 5
  batch_example = tf.train.shuffle_batch(
        [serialized_example], batch_size, capacity,
        MIN_AFTER_DEQUEUE)
  features = tf.parse_example(
      batch_example,
      features={
        'target': tf.FixedLenFeature(shape=[1],
                                     dtype=tf.float32,
                                     default_value=[-1]),
        'inputs': tf.FixedLenFeature(shape=[1], dtype=tf.float32),
      })

  targets = features['target']  
  inputs = features['inputs']

  # The initial value should be such that type is correctly inferred as
  # float.
  weights = tf.Variable([0.0], name='weights')  
  outputs = tf.add(inputs, tf.negative(weights))
  
  diff = targets - outputs
  error = tf.reduce_mean(diff * diff)
  loss = tf.reduce_mean(error, name='loss')
  input_mean = tf.reshape(tf.reduce_mean(inputs), [1])
  update_weights = weights.assign(input_mean)

  # Add a global step and increment it at the same time we do the assignment.
  # This will become our "train" op.
  global_step = tf.Variable(0, name='global_step', trainable=False)
  with tf.control_dependencies([update_weights]):
    train = global_step.assign_add(tf.constant(
        1, global_step.dtype))  
  return GraphOps(weights=weights, global_step=global_step, train=train, inputs=inputs, targets=targets)


def main(args): 
  """Run training
  
  Args:
    args: Object containing the command line arguments.
  """
  server = None
  device_func = None
  if args.cluster_spec:
    cluster_spec_dict = json.loads(args.cluster_spec)
    cluster_spec = tf.train.ClusterSpec(cluster_spec_dict)
    server_def = tf.train.ServerDef(cluster=cluster_spec.as_cluster_def(),
                                    protocol="grpc",
                                    job_name=args.job_name,
                                    task_index=args.task_index)

    logging.info("server_def: %s", server_def)

    logging.info("Building server.")
    # Create and start a server for the local task.
    server = tf.train.Server(server_def)
    logging.info("Finished building server.")

    # Assigns ops to the local worker by default.
    device_func = tf.train.replica_device_setter(
        worker_device="/job:worker/task:%d" % server_def.task_index,
        cluster=server_def.cluster)
    is_chief = (args.task_index == 0)
  else:
    # This should return a null op device setter since we are using
    # all the defaults.
    logging.info("Using default device function.")
    device_func = tf.train.replica_device_setter()
    is_chief = True

  if args.job_name == "ps":
    server.join()
  elif args.job_name == "worker" or not args.job_name:
    with tf.device(device_func):
      run(server=server, train_data_paths=args.train_data_paths, output_path=args.output_path,
          is_chief=is_chief)
  elif args.job_name == "evaluator":
    raise ValueError("Adding an evaluator job is not currently supported.")
  else:
    raise ValueError("invalid job_type %s" % (args.job_type,))


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  args = parse_args()
  main(args)
