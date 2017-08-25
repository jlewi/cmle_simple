"""A script for submitting an running_average model to the cloud for use in prediction."""

import argparse
import datetime
import google.cloud.ml.util._api as _api
import logging
import pytz
import IPython

MODEL_NAME = 'running_average'

if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  timezone = pytz.timezone('US/Pacific')
  now = datetime.datetime.now(timezone)
  
  parser = argparse.ArgumentParser(
      description='Deploys the running_average model to the Cloud.')
  parser.add_argument('--project_id',
                      required=True,
                      help='The project to which the job will be submitted.')
  parser.add_argument('--version',
                      default=now.strftime("v%y%m%d_%H%M%S"),
                      help=('The version of the model to deploy. If omitted, '
                            'a default value will be supplied.'))
  parser.add_argument('--origin_uri',
                      required=True,
                      help='The GCS ordirectory in which the model resides.')
  parser.add_argument('--endpoint',
                      help='(Optional) Endpoint to use.')
  args = parser.parse_args()
  
  version = args.version
  
  api = _api.ApiV3(project_id=args.project_id, endpoint=args.endpoint)
  response = api.create_model(MODEL_NAME)
  logging.info("Create Model Response: %s", response)
  response = api.deploy_version(MODEL_NAME, version, args.origin_uri)
  logging.info("Deploy Version Response: %s", response)