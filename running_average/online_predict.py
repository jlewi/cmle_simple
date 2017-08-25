"""A script for generating some online predictions."""

import argparse
import datetime
import google.cloud.ml.util._api as _api
import json
import logging
import pytz
import IPython

MODEL_NAME = 'running_average'

if __name__ == "__main__":
  logging.getLogger().setLevel(logging.INFO)
  timezone = pytz.timezone('US/Pacific')
  now = datetime.datetime.now(timezone)
  
  parser = argparse.ArgumentParser(
      description='Run some online prediction the running_average model to the Cloud.')
  parser.add_argument('--project_id',
                      required=True,
                      help='The project to which the job will be submitted.')
  parser.add_argument('--version',
                      default=now.strftime("v%y%m%d_%H%M%S"),
                      help='The version of the model to use.')
  parser.add_argument('--model',
                      required=True,
                      help='The name of the model.')
  parser.add_argument('--endpoint',
                      help='(Optional) Endpoint to use.')
  args = parser.parse_args()
  
  version = args.version
  
  api = _api.ApiV3(project_id=args.project_id, endpoint=args.endpoint)
  instances =[]
  for index in range(10):
    record = {
      'inputs': index,
    }
    instances.append(json.dumps(record))

  print instances
  print api.predict(model_name=args.model, model_version=args.version,
    instances=instances)