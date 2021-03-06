# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/cmle_example.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/cmle_example.proto',
  package='cmle.example',
  syntax='proto3',
  serialized_pb=_b('\n\x16\x61pi/cmle_example.proto\x12\x0c\x63mle.example\"\x1f\n\x0ePredictRequest\x12\r\n\x05input\x18\x01 \x01(\x02\"!\n\x0fPredictResponse\x12\x0e\n\x06output\x18\x01 \x01(\x02\x32W\n\x0b\x43mleExample\x12H\n\x07Predict\x12\x1c.cmle.example.PredictRequest\x1a\x1d.cmle.example.PredictResponse\"\x00\x62\x06proto3')
)




_PREDICTREQUEST = _descriptor.Descriptor(
  name='PredictRequest',
  full_name='cmle.example.PredictRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='input', full_name='cmle.example.PredictRequest.input', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=71,
)


_PREDICTRESPONSE = _descriptor.Descriptor(
  name='PredictResponse',
  full_name='cmle.example.PredictResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='cmle.example.PredictResponse.output', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['PredictRequest'] = _PREDICTREQUEST
DESCRIPTOR.message_types_by_name['PredictResponse'] = _PREDICTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PredictRequest = _reflection.GeneratedProtocolMessageType('PredictRequest', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTREQUEST,
  __module__ = 'api.cmle_example_pb2'
  # @@protoc_insertion_point(class_scope:cmle.example.PredictRequest)
  ))
_sym_db.RegisterMessage(PredictRequest)

PredictResponse = _reflection.GeneratedProtocolMessageType('PredictResponse', (_message.Message,), dict(
  DESCRIPTOR = _PREDICTRESPONSE,
  __module__ = 'api.cmle_example_pb2'
  # @@protoc_insertion_point(class_scope:cmle.example.PredictResponse)
  ))
_sym_db.RegisterMessage(PredictResponse)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities


  class CmleExampleStub(object):
    """The CmleExample service definition.
    """

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.Predict = channel.unary_unary(
          '/cmle.example.CmleExample/Predict',
          request_serializer=PredictRequest.SerializeToString,
          response_deserializer=PredictResponse.FromString,
          )


  class CmleExampleServicer(object):
    """The CmleExample service definition.
    """

    def Predict(self, request, context):
      """Sends a prediction request
      """
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_CmleExampleServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Predict': grpc.unary_unary_rpc_method_handler(
            servicer.Predict,
            request_deserializer=PredictRequest.FromString,
            response_serializer=PredictResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'cmle.example.CmleExample', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaCmleExampleServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """The CmleExample service definition.
    """
    def Predict(self, request, context):
      """Sends a prediction request
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaCmleExampleStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    """The CmleExample service definition.
    """
    def Predict(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      """Sends a prediction request
      """
      raise NotImplementedError()
    Predict.future = None


  def beta_create_CmleExample_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('cmle.example.CmleExample', 'Predict'): PredictRequest.FromString,
    }
    response_serializers = {
      ('cmle.example.CmleExample', 'Predict'): PredictResponse.SerializeToString,
    }
    method_implementations = {
      ('cmle.example.CmleExample', 'Predict'): face_utilities.unary_unary_inline(servicer.Predict),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_CmleExample_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('cmle.example.CmleExample', 'Predict'): PredictRequest.SerializeToString,
    }
    response_deserializers = {
      ('cmle.example.CmleExample', 'Predict'): PredictResponse.FromString,
    }
    cardinalities = {
      'Predict': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'cmle.example.CmleExample', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
