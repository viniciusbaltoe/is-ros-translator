# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: is_ros.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='is_ros.proto',
  package='is.ros',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0cis_ros.proto\x12\x06is.ros\x1a\x19google/protobuf/any.proto\"Y\n\x13ROSTranslateRequest\x12\r\n\x05topic\x18\x01 \x01(\t\x12!\n\x03\x61ny\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x10\n\x08\x66unction\x18\x03 \x01(\t\"D\n\x11ROSTranslateReply\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\x12!\n\x03\x61ny\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Anyb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,])




_ROSTRANSLATEREQUEST = _descriptor.Descriptor(
  name='ROSTranslateRequest',
  full_name='is.ros.ROSTranslateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='topic', full_name='is.ros.ROSTranslateRequest.topic', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='any', full_name='is.ros.ROSTranslateRequest.any', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function', full_name='is.ros.ROSTranslateRequest.function', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=140,
)


_ROSTRANSLATEREPLY = _descriptor.Descriptor(
  name='ROSTranslateReply',
  full_name='is.ros.ROSTranslateReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='is.ros.ROSTranslateReply.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='any', full_name='is.ros.ROSTranslateReply.any', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=210,
)

_ROSTRANSLATEREQUEST.fields_by_name['any'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_ROSTRANSLATEREPLY.fields_by_name['any'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['ROSTranslateRequest'] = _ROSTRANSLATEREQUEST
DESCRIPTOR.message_types_by_name['ROSTranslateReply'] = _ROSTRANSLATEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ROSTranslateRequest = _reflection.GeneratedProtocolMessageType('ROSTranslateRequest', (_message.Message,), dict(
  DESCRIPTOR = _ROSTRANSLATEREQUEST,
  __module__ = 'is_ros_pb2'
  # @@protoc_insertion_point(class_scope:is.ros.ROSTranslateRequest)
  ))
_sym_db.RegisterMessage(ROSTranslateRequest)

ROSTranslateReply = _reflection.GeneratedProtocolMessageType('ROSTranslateReply', (_message.Message,), dict(
  DESCRIPTOR = _ROSTRANSLATEREPLY,
  __module__ = 'is_ros_pb2'
  # @@protoc_insertion_point(class_scope:is.ros.ROSTranslateReply)
  ))
_sym_db.RegisterMessage(ROSTranslateReply)


# @@protoc_insertion_point(module_scope)
