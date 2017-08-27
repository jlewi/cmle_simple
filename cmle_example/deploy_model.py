"""A script for submitting an running_average model to the cloud for use in prediction."""

import argparse
import datetime
import json
import logging
import pytz

from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient import http
from oauth2client.client import GoogleCredentials
from cmle_example import util

MODEL_NAME = 'cmle_example'

def deploy(project_id, model_path, model_name, model_version, runtime_version='1.2', endpoint=None):
  """Deply the model.

  Args:
      project_id: Id of the project.
      model_path: The path to the directory containing the saved model protocol buffer.
      model_name: The name for the model.
      model_version: The version for the model.
      runtime_version: The Tensorflow runtime version to use.

  Returns:
      response from create version.
  """
  cloudml = discovery.build(
      'ml',
      'v1',
      requestBuilder=http.HttpRequest)

  if endpoint:
      cloudml._baseUrl = endpoint  # pylint: disable=protected-access

  create_request = {
    "name": model_name,
    "description": "Simple CMLE Example model",
  }
  models = cloudml.projects().models()
  request = models.create(
      body=create_request, parent='projects/' + project_id)

  try:
    response = request.execute()
    logging.info('Set response:\n%s', util.PrettyFormat(response))
  except errors.HttpError as e:
    content = json.loads(e.content)
    if content['error']['status'] == 'ALREADY_EXISTS':
      logging.info('Model %s already exists.', model_name)
    else:
      logging.error('Job submission failed: %s', e)
      # If running on corp response will contain BNS of the backend that was
      # hit which is very useful for debugging.
      pretty_resp = json.dumps(e.resp, sort_keys=True, indent=4,
                               separators=(',', ': '))
      logging.error('Response Headers: %s', pretty_resp)


  # Create the version.
  versions = cloudml.projects().models().versions()
  create_version_request = {
    "name": model_version,
    "deploymentUri": model_path,
    "runtimeVersion": "1.2",
  }
  request =  versions.create(
      body=create_version_request, parent='projects/{0}/models/{1}'.format(project_id, model_name))

  try:
    response = request.execute()
    logging.info('Set response:\n%s', util.PrettyFormat(response))
  except errors.HttpError as e:
    content = json.loads(e.content)
    if content['error']['status'] == 'ALREADY_EXISTS':
      logging.error('Model Version %s already exists.', model_version)
    else:
      logging.error('Job submission failed: %s', e)
      # If running on corp response will contain BNS of the backend that was
      # hit which is very useful for debugging.
      pretty_resp = json.dumps(e.resp, sort_keys=True, indent=4,
                               separators=(',', ': '))
      logging.error('Response Headers: %s', pretty_resp)

  return response

if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  timezone = pytz.timezone('US/Pacific')
  now = datetime.datetime.now(timezone)
  
  parser = argparse.ArgumentParser(
      description='Deploys the running_average model to the Cloud.')
  parser.add_argument('--project_id',
                      required=True,
                      help='The project to which the job will be submitted.')

  parser.add_argument('--model_name',
                      default=now.strftime("simple_cmle"),
                      help=('The name for the deployed model. If omitted, '
                            'a default value will be supplied.'))

  parser.add_argument('--version',
                      default=now.strftime("v%y%m%d_%H%M%S"),
                      help=('The version of the model to deploy. If omitted, '
                            'a default value will be supplied.'))
  parser.add_argument('--model_path',
                      required=True,
                      help='The GCS or directory in which the model resides.')
  parser.add_argument('--endpoint',
                      help='(Optional) Endpoint to use.')
  args = parser.parse_args()
  
  version = args.version

  deploy(args.project_id, args.model_path, args.model_name, args.model_version)