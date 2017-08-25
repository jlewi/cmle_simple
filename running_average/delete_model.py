"""A script for deleting a running_average model in the cloud."""

import argparse
import datetime
from google.cloud.ml.util import _api
from google.cloud.ml.util import _http
import logging
import pytz
import IPython

MODEL_NAME = 'running_average'


if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  timezone = pytz.timezone('US/Pacific')
  now = datetime.datetime.now(timezone)
  
  parser = argparse.ArgumentParser(
      description='Delete the running_average model.')
  parser.add_argument('--project_id',
                      required=True,
                      help='The project to which the job will be submitted.')
  parser.add_argument('--endpoint',
                      help='(Optional) Endpoint to use.')                      
  args = parser.parse_args()
  
  api = ApiV3Modified(project_id=args.project_id, endpoint=args.endpoint)
  response = api.delete_model(MODEL_NAME)
  logging.info("Delete Model Response: %s", response)