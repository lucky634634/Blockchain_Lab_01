# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import Raft_pb2 as Raft__pb2

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
        + f' but the generated code in Raft_pb2_grpc.py depends on'
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
        self.SetIsActive = channel.unary_unary(
                '/Raft/SetIsActive',
                request_serializer=Raft__pb2.SetIsActiveRequest.SerializeToString,
                response_deserializer=Raft__pb2.SetIsActiveResponse.FromString,
                _registered_method=True)
        self.GetIsActive = channel.unary_unary(
                '/Raft/GetIsActive',
                request_serializer=Raft__pb2.GetIsActiveRequest.SerializeToString,
                response_deserializer=Raft__pb2.GetIsActiveResponse.FromString,
                _registered_method=True)
        self.Stop = channel.unary_unary(
                '/Raft/Stop',
                request_serializer=Raft__pb2.StopRequest.SerializeToString,
                response_deserializer=Raft__pb2.StopResponse.FromString,
                _registered_method=True)
        self.GetRole = channel.unary_unary(
                '/Raft/GetRole',
                request_serializer=Raft__pb2.GetRoleRequest.SerializeToString,
                response_deserializer=Raft__pb2.GetRoleResponse.FromString,
                _registered_method=True)
        self.RequestVote = channel.unary_unary(
                '/Raft/RequestVote',
                request_serializer=Raft__pb2.RequestVoteRequest.SerializeToString,
                response_deserializer=Raft__pb2.RequestVoteResponse.FromString,
                _registered_method=True)
        self.AppendEntries = channel.unary_unary(
                '/Raft/AppendEntries',
                request_serializer=Raft__pb2.AppendEntriesRequest.SerializeToString,
                response_deserializer=Raft__pb2.AppendEntriesResponse.FromString,
                _registered_method=True)
        self.AddPeer = channel.unary_unary(
                '/Raft/AddPeer',
                request_serializer=Raft__pb2.AddPeerRequest.SerializeToString,
                response_deserializer=Raft__pb2.AddPeerResponse.FromString,
                _registered_method=True)
        self.RemovePeer = channel.unary_unary(
                '/Raft/RemovePeer',
                request_serializer=Raft__pb2.RemovePeerRequest.SerializeToString,
                response_deserializer=Raft__pb2.RemovePeerResponse.FromString,
                _registered_method=True)
        self.SendCommand = channel.unary_unary(
                '/Raft/SendCommand',
                request_serializer=Raft__pb2.SendCommandRequest.SerializeToString,
                response_deserializer=Raft__pb2.SendCommandResponse.FromString,
                _registered_method=True)


class RaftServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetIsActive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIsActive(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

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

    def AddPeer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemovePeer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RaftServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetIsActive': grpc.unary_unary_rpc_method_handler(
                    servicer.SetIsActive,
                    request_deserializer=Raft__pb2.SetIsActiveRequest.FromString,
                    response_serializer=Raft__pb2.SetIsActiveResponse.SerializeToString,
            ),
            'GetIsActive': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIsActive,
                    request_deserializer=Raft__pb2.GetIsActiveRequest.FromString,
                    response_serializer=Raft__pb2.GetIsActiveResponse.SerializeToString,
            ),
            'Stop': grpc.unary_unary_rpc_method_handler(
                    servicer.Stop,
                    request_deserializer=Raft__pb2.StopRequest.FromString,
                    response_serializer=Raft__pb2.StopResponse.SerializeToString,
            ),
            'GetRole': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRole,
                    request_deserializer=Raft__pb2.GetRoleRequest.FromString,
                    response_serializer=Raft__pb2.GetRoleResponse.SerializeToString,
            ),
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=Raft__pb2.RequestVoteRequest.FromString,
                    response_serializer=Raft__pb2.RequestVoteResponse.SerializeToString,
            ),
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=Raft__pb2.AppendEntriesRequest.FromString,
                    response_serializer=Raft__pb2.AppendEntriesResponse.SerializeToString,
            ),
            'AddPeer': grpc.unary_unary_rpc_method_handler(
                    servicer.AddPeer,
                    request_deserializer=Raft__pb2.AddPeerRequest.FromString,
                    response_serializer=Raft__pb2.AddPeerResponse.SerializeToString,
            ),
            'RemovePeer': grpc.unary_unary_rpc_method_handler(
                    servicer.RemovePeer,
                    request_deserializer=Raft__pb2.RemovePeerRequest.FromString,
                    response_serializer=Raft__pb2.RemovePeerResponse.SerializeToString,
            ),
            'SendCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.SendCommand,
                    request_deserializer=Raft__pb2.SendCommandRequest.FromString,
                    response_serializer=Raft__pb2.SendCommandResponse.SerializeToString,
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
    def SetIsActive(request,
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
            '/Raft/SetIsActive',
            Raft__pb2.SetIsActiveRequest.SerializeToString,
            Raft__pb2.SetIsActiveResponse.FromString,
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
    def GetIsActive(request,
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
            '/Raft/GetIsActive',
            Raft__pb2.GetIsActiveRequest.SerializeToString,
            Raft__pb2.GetIsActiveResponse.FromString,
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
    def Stop(request,
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
            '/Raft/Stop',
            Raft__pb2.StopRequest.SerializeToString,
            Raft__pb2.StopResponse.FromString,
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
    def GetRole(request,
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
            '/Raft/GetRole',
            Raft__pb2.GetRoleRequest.SerializeToString,
            Raft__pb2.GetRoleResponse.FromString,
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
            Raft__pb2.RequestVoteRequest.SerializeToString,
            Raft__pb2.RequestVoteResponse.FromString,
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
            Raft__pb2.AppendEntriesRequest.SerializeToString,
            Raft__pb2.AppendEntriesResponse.FromString,
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
    def AddPeer(request,
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
            '/Raft/AddPeer',
            Raft__pb2.AddPeerRequest.SerializeToString,
            Raft__pb2.AddPeerResponse.FromString,
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
    def RemovePeer(request,
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
            '/Raft/RemovePeer',
            Raft__pb2.RemovePeerRequest.SerializeToString,
            Raft__pb2.RemovePeerResponse.FromString,
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
    def SendCommand(request,
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
            '/Raft/SendCommand',
            Raft__pb2.SendCommandRequest.SerializeToString,
            Raft__pb2.SendCommandResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
