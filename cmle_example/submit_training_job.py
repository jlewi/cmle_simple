"""Submit training job to the Cloud ML service."""

import argparse
import datetime
import getpass
import glob
import json
import logging
import os

import google.cloud.storage as gcs
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient import http
from oauth2client.client import GoogleCredentials

from cmle_example import util


import pytz
import subprocess
import tempfile

import re

GcsPattern = re.compile(r"gs://([^/]*)/(.*)")

def submit_job(job_name, main_args, output_path, project_id, endpoint=None):
  # Build the setup package.
  source_dir = os.path.dirname(__file__)
  setup_dir = os.path.abspath(os.path.join(source_dir, os.pardir))
  setup_path = os.path.join(setup_dir, "setup.py")
  dist_dir = tempfile.mkdtemp()
  logging.info("Setup file: %s", setup_path)
  subprocess.check_call(["python", setup_path, "sdist", "--dist-dir=" + dist_dir])
  
  glob_path = os.path.join(dist_dir, "*.tar.gz")
  packages = glob.glob(glob_path)
  
  logging.info("Found packages: %s", packages)
  if not packages:
    raise ValueError("No packages matched glob: %s" % glob_path)

  gcs_client = gcs.Client(project_id)

  # Copy the code to GCS  
  gcs_packages = []
  bucket = None
  for p in packages:
    dest = os.path.join(output_path,
                        'staging', os.path.basename(p))


    m = GcsPattern.match(dest)
    if not m:
        raise ValueError("Not a  GCS package %s" % dest)
    bucket_name = m.group(1)
    obj_path = m.group(2)
    if not bucket or bucket_name != bucket.name:
        bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob(obj_path)

    logging.info('Copying %s to %s', p, dest)
    blob.upload_from_filename(p)
    gcs_packages.append(dest)


  credentials = GoogleCredentials.get_application_default()
  
  cloudml = discovery.build(
      'ml',
      'v1',
      requestBuilder=http.HttpRequest,
      credentials=credentials)

  if endpoint:
    cloudml._baseUrl = endpoint  # pylint: disable=protected-access

  output_path = output_path
  if not output_path:
    output_path = "gs://{0}_{1}/running_average/{2}/output".format(
        project_id, getpass.getuser(), now.strftime("%y%m%d_%H%M%S"))

  main_args.append("--output_path={0}".format(output_path))
  job_request = {
      'job_id': job_name,
      'training_input': {
         'scale_tier': 'STANDARD_1',
         'package_uris': gcs_packages,
         'python_module': 'cmle_example.train',
         'region': 'us-central1',
         'args': main_args,
          'runtimeVersion': '1.2',
      }
  }
  jobs = cloudml.projects().jobs()
  request = jobs.create(
      body=job_request, parent='projects/' + project_id)

  try:
    response = request.execute()
    logging.info('Set response:\n%s', util.PrettyFormat(response))
  except errors.HttpError as e:
    logging.error('Job submission failed: %s', e)
    # If running on corp response will contain BNS of the backend that was
    # hit which is very useful for debugging.
    pretty_resp = json.dumps(e.resp, sort_keys=True, indent=4,
                             separators=(',', ': '))
    logging.error('Response Headers: %s', pretty_resp)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  timezone = pytz.timezone('US/Pacific')
  now = datetime.datetime.now(timezone)
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--job_name',
                      default=now.strftime('running_average_{0}_%y%m%d_%H%M%S'.format(
                          getpass.getuser())),
                      help=('(Optional) job name. If not specified one will be '
                            'chosen automatically.'))
  parser.add_argument('--output_path',
                      required=True,
                      help='The GCS path to which output will be written.')
  parser.add_argument('--project_id',
                      default='dataflow-jlewi',
                      help='The project to which the job will be submitted.')
  parser.add_argument('--endpoint',
                      default=None,
                      help='Cloud ML Endpoint.')

  # Parse the arguments. Unknown arguments will be treated as arguments of the program.
  args, main_args = parser.parse_known_args()

  submit_job(args.job_name, main_args, args.output_path, args.project_id, args.endpoint)