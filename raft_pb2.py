# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: raft.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'raft.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"b\n\x12RequestVoteRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"8\n\x13RequestVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08\"\x93\x01\n\x14\x41ppendEntriesRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\x05\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1a\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\t.LogEntry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\")\n\x08LogEntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\"\"\n\x10SetActiveRequest\x12\x0e\n\x06\x61\x63tive\x18\x01 \x01(\x08\"$\n\x11SetActiveResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x12\n\x10GetActiveRequest\"#\n\x11GetActiveResponse\x12\x0e\n\x06\x61\x63tive\x18\x01 \x01(\x08\x32\xe8\x01\n\x04Raft\x12\x38\n\x0bRequestVote\x12\x13.RequestVoteRequest\x1a\x14.RequestVoteResponse\x12>\n\rAppendEntries\x12\x15.AppendEntriesRequest\x1a\x16.AppendEntriesResponse\x12\x32\n\tSetActive\x12\x11.SetActiveRequest\x1a\x12.SetActiveResponse\x12\x32\n\tGetActive\x12\x11.GetActiveRequest\x1a\x12.GetActiveResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REQUESTVOTEREQUEST']._serialized_start=14
  _globals['_REQUESTVOTEREQUEST']._serialized_end=112
  _globals['_REQUESTVOTERESPONSE']._serialized_start=114
  _globals['_REQUESTVOTERESPONSE']._serialized_end=170
  _globals['_APPENDENTRIESREQUEST']._serialized_start=173
  _globals['_APPENDENTRIESREQUEST']._serialized_end=320
  _globals['_APPENDENTRIESRESPONSE']._serialized_start=322
  _globals['_APPENDENTRIESRESPONSE']._serialized_end=376
  _globals['_LOGENTRY']._serialized_start=378
  _globals['_LOGENTRY']._serialized_end=419
  _globals['_SETACTIVEREQUEST']._serialized_start=421
  _globals['_SETACTIVEREQUEST']._serialized_end=455
  _globals['_SETACTIVERESPONSE']._serialized_start=457
  _globals['_SETACTIVERESPONSE']._serialized_end=493
  _globals['_GETACTIVEREQUEST']._serialized_start=495
  _globals['_GETACTIVEREQUEST']._serialized_end=513
  _globals['_GETACTIVERESPONSE']._serialized_start=515
  _globals['_GETACTIVERESPONSE']._serialized_end=550
  _globals['_RAFT']._serialized_start=553
  _globals['_RAFT']._serialized_end=785
# @@protoc_insertion_point(module_scope)
