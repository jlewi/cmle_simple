"""Submit training job to the Cloud ML service."""

import argparse
import datetime
import getpass
import glob
import json
import logging
import os

import google.cloud.ml.util._file as ml_file
import google.cloud.ml.util._api as ml_api
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient import http
from oauth2client.client import GoogleCredentials

import pytz
import subprocess
import tempfile

def PrettyFormat(d):
    return json.dumps(d, sort_keys=True,
                      indent=2, separators=(',', ': '))

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
    
  # Copy the code to GCS  
  gcs_packages = []
  for p in packages:
    dest = os.path.join(output_path,
                        'staging', os.path.basename(p))

    logging.info('Copying %s to %s', p, dest)
    ml_file.copy_file(p, dest)
    gcs_packages.append(dest)


  credentials = GoogleCredentials.get_application_default()
  
  cloudml = discovery.build(
      'ml',
      'v1beta1',
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
         'python_module': 'running_average.running_average_main',
         'region': 'us-central1',
         'args': main_args,
      }
  }
  jobs = cloudml.projects().jobs()
  request = jobs.create(
      body=job_request, parent='projects/' + project_id)

  try:
    response = request.execute()
    logging.info('Set response:\n%s', PrettyFormat(response))
  except errors.HttpError as e:
    logging.error('Job submission failed: %s', e)
    # If running on corp response will contain BNS of the backend that was
    # hit which is very useful for debugging.
    pretty_resp = json.dumps(e.resp, sort_keys=True, indent=4,
                             separators=(',', ': '))
    logging.error('Response Headers: %s', pretty_resp)

  # Poll the job until its done.
  api = ml_api.ApiBeta(credential=credentials, project_id=project_id)
  final_job = api.wait_for_job(job_name)
  logging.info('Job status:\n %s', PrettyFormat(final_job))
  if final_job['state'] in ['RUNNING', 'QUEUED', 'CANCELLING', 'PREPARING']:
    msg = ('The training job {0} did not complete in the time '
           'allotted.').format(job_name)
    logging.error(msg)
  else:
    # The job completed. So now we need to check whether it completed
    # successfully or with an error.
    if final_job['state'] != "SUCCEEDED":
      # The job finished with an error.
      msg = 'The training job {0} finished with {1} error: {1}.'.format(
          job_name, final_job['errorMessage'])
      logging.error(msg)
    else:
      logging.info('Job completed successfully')

    return final_job

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

  submit_job(args.job_name, main_args, args.output_path, args,project_id, args.endpoint)