# A Simple Example

* A toy TensorFlow model for experimenting with various aspects of CMLE.

See the Datalab notebook cmle_example.ipynb for more information on training
and deploying a model.


## Setting up an API using Cloud Endpoints

The notebook [cmle_example.ipynb](cmle_example.ipynb) contains commands
to deploy an API using Cloud Endpoints.

However, you will need to use a special Datalab container that contains
additional dependencies such as the protoc compiler. You can build
this docker image with the following command.

```
./images/datalab/build_and_push.py --project=$PROJECT
```
