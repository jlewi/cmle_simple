# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python gRPC CMLE Server Example."""

import argparse
import http
import logging
import time

from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient import http

from google.rpc import code_pb2
from cmle_example.api import cmle_example_pb2
import status

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class CmleExampleServicer(cmle_example_pb2.CmleExampleServicer):
  """Implements the CMLE Example API server."""
  def __init__(self, project, model_name, model_version):
    self.project = project
    self.model_name = model_name
    self.model_version = model_version

    self.cloudml = discovery.build(
      'ml',
      'v1',
      requestBuilder=http.HttpRequest)

    # TODO(jlewi): We should verify the model exists on startup.

  def Predict(self, request, context):
    with status.context(context):
      print("request {0}".format(request))
      projects = self.cloudml.projects()

      body = {
        'instances': [
          {
            'inputs': [request.input],
          },
        ],
      }
      cmle_request = projects.predict(
        name='projects/{0}/models/{1}/versions/{2}'.format(self.project, self.model_name, self.model_version),
        body=body)

      response = cmle_example_pb2.PredictResponse()
      try:
        json_response = cmle_request.execute()
      except errors.HttpError as e:
        logging.error("There was a problem issuing the CMLE predict request: %s", e)

        context.code(code_pb2.UNAVAILABLE)
        context.details(
          'There was a problem issuing the CMLE predict request {}'.format(e))

        return response
      response.output = json_response["predictions"][0]["outputs"][0]

      # TODO(jlewi): Need to issue an actual predict request.
      return response


def serve(port, shutdown_grace_duration, project, model_name, model_version):
  """Configures and runs the bookstore API server."""
  server = cmle_example_pb2.beta_create_CmleExample_server(
    CmleExampleServicer(project, model_name, model_version))
  server.add_insecure_port('[::]:{}'.format(port))
  server.start()

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(shutdown_grace_duration)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument(
    '--port', type=int, default=8000, help='The port to listen on')
  parser.add_argument(
    '--shutdown_grace_duration', type=int, default=5,
    help='The shutdown grace duration, in seconds')
  parser.add_argument(
    '--project', type=str, help='The project that owns the model to use for predictions.',
    required=True,
  )
  parser.add_argument(
    '--model_name', type=str, help='The name of the model to use for predictions.',
    required=True,
  )
  parser.add_argument(
    '--model_version', type=str, help='The model version to use for predictions.',
    required=True,
  )

  args = parser.parse_args()

  serve(args.port, args.shutdown_grace_duration, args.project, args.model_name, args.model_version)