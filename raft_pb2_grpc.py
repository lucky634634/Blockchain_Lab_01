# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import raft_pb2 as raft__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in raft_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RaftStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestVote = channel.unary_unary(
                '/Raft/RequestVote',
                request_serializer=raft__pb2.RequestVoteRequest.SerializeToString,
                response_deserializer=raft__pb2.RequestVoteResponse.FromString,
                _registered_method=True)
        self.AppendEntries = channel.unary_unary(
                '/Raft/AppendEntries',
                request_serializer=raft__pb2.AppendEntriesRequest.SerializeToString,
                response_deserializer=raft__pb2.AppendEntriesResponse.FromString,
                _registered_method=True)
        self.SetActive = channel.unary_unary(
                '/Raft/SetActive',
                request_serializer=raft__pb2.SetActiveRequest.SerializeToString,
                response_deserializer=raft__pb2.SetActiveResponse.FromString,
                _registered_method=True)
        self.GetActive = channel.unary_unary(
                '/Raft/GetActive',
                request_serializer=raft__pb2.GetActiveRequest.SerializeToString,
                response_deserializer=raft__pb2.GetActiveResponse.FromString,
                _registered_method=True)


class RaftServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetActive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetActive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RaftServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.RequestVoteRequest.FromString,
                    response_serializer=raft__pb2.RequestVoteResponse.SerializeToString,
            ),
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=raft__pb2.AppendEntriesRequest.FromString,
                    response_serializer=raft__pb2.AppendEntriesResponse.SerializeToString,
            ),
            'SetActive': grpc.unary_unary_rpc_method_handler(
                    servicer.SetActive,
                    request_deserializer=raft__pb2.SetActiveRequest.FromString,
                    response_serializer=raft__pb2.SetActiveResponse.SerializeToString,
            ),
            'GetActive': grpc.unary_unary_rpc_method_handler(
                    servicer.GetActive,
                    request_deserializer=raft__pb2.GetActiveRequest.FromString,
                    response_serializer=raft__pb2.GetActiveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Raft', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Raft', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Raft(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Raft/RequestVote',
            raft__pb2.RequestVoteRequest.SerializeToString,
            raft__pb2.RequestVoteResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AppendEntries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Raft/AppendEntries',
            raft__pb2.AppendEntriesRequest.SerializeToString,
            raft__pb2.AppendEntriesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetActive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Raft/SetActive',
            raft__pb2.SetActiveRequest.SerializeToString,
            raft__pb2.SetActiveResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetActive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Raft/GetActive',
            raft__pb2.GetActiveRequest.SerializeToString,
            raft__pb2.GetActiveResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
