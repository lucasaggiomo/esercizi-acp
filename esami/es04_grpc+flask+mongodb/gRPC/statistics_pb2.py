# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: statistics.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10statistics.proto\x12\nstatistics\"\x07\n\x05\x45mpty\"(\n\x06Sensor\x12\x0b\n\x03_id\x18\x01 \x01(\x05\x12\x11\n\tdata_type\x18\x02 \x01(\t\"3\n\x0bMeanRequest\x12\x11\n\tsensor_id\x18\x01 \x01(\x05\x12\x11\n\tdata_type\x18\x02 \x01(\t\"\x1e\n\rStringMessage\x12\r\n\x05value\x18\x01 \x01(\t2\x89\x01\n\x11StatisticsService\x12\x35\n\ngetSensors\x12\x11.statistics.Empty\x1a\x12.statistics.Sensor0\x01\x12=\n\x07getMean\x12\x17.statistics.MeanRequest\x1a\x19.statistics.StringMessageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'statistics_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=32
  _globals['_EMPTY']._serialized_end=39
  _globals['_SENSOR']._serialized_start=41
  _globals['_SENSOR']._serialized_end=81
  _globals['_MEANREQUEST']._serialized_start=83
  _globals['_MEANREQUEST']._serialized_end=134
  _globals['_STRINGMESSAGE']._serialized_start=136
  _globals['_STRINGMESSAGE']._serialized_end=166
  _globals['_STATISTICSSERVICE']._serialized_start=169
  _globals['_STATISTICSSERVICE']._serialized_end=306
# @@protoc_insertion_point(module_scope)
