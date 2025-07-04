# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import orderManager_pb2 as orderManager__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in orderManager_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class OrderManagerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.addOrder = channel.unary_unary(
                '/orderManager.OrderManagerService/addOrder',
                request_serializer=orderManager__pb2.Order.SerializeToString,
                response_deserializer=orderManager__pb2.StringMessage.FromString,
                _registered_method=True)
        self.getOrder = channel.unary_unary(
                '/orderManager.OrderManagerService/getOrder',
                request_serializer=orderManager__pb2.StringMessage.SerializeToString,
                response_deserializer=orderManager__pb2.Order.FromString,
                _registered_method=True)
        self.searchOrders = channel.unary_stream(
                '/orderManager.OrderManagerService/searchOrders',
                request_serializer=orderManager__pb2.StringMessage.SerializeToString,
                response_deserializer=orderManager__pb2.Order.FromString,
                _registered_method=True)
        self.processOrders = channel.stream_stream(
                '/orderManager.OrderManagerService/processOrders',
                request_serializer=orderManager__pb2.Order.SerializeToString,
                response_deserializer=orderManager__pb2.CombinedShipment.FromString,
                _registered_method=True)
        self.cancelShipment = channel.unary_unary(
                '/orderManager.OrderManagerService/cancelShipment',
                request_serializer=orderManager__pb2.StringMessage.SerializeToString,
                response_deserializer=orderManager__pb2.StringMessage.FromString,
                _registered_method=True)


class OrderManagerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def addOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def searchOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def processOrders(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cancelShipment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderManagerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'addOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.addOrder,
                    request_deserializer=orderManager__pb2.Order.FromString,
                    response_serializer=orderManager__pb2.StringMessage.SerializeToString,
            ),
            'getOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.getOrder,
                    request_deserializer=orderManager__pb2.StringMessage.FromString,
                    response_serializer=orderManager__pb2.Order.SerializeToString,
            ),
            'searchOrders': grpc.unary_stream_rpc_method_handler(
                    servicer.searchOrders,
                    request_deserializer=orderManager__pb2.StringMessage.FromString,
                    response_serializer=orderManager__pb2.Order.SerializeToString,
            ),
            'processOrders': grpc.stream_stream_rpc_method_handler(
                    servicer.processOrders,
                    request_deserializer=orderManager__pb2.Order.FromString,
                    response_serializer=orderManager__pb2.CombinedShipment.SerializeToString,
            ),
            'cancelShipment': grpc.unary_unary_rpc_method_handler(
                    servicer.cancelShipment,
                    request_deserializer=orderManager__pb2.StringMessage.FromString,
                    response_serializer=orderManager__pb2.StringMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'orderManager.OrderManagerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('orderManager.OrderManagerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class OrderManagerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def addOrder(request,
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
            '/orderManager.OrderManagerService/addOrder',
            orderManager__pb2.Order.SerializeToString,
            orderManager__pb2.StringMessage.FromString,
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
    def getOrder(request,
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
            '/orderManager.OrderManagerService/getOrder',
            orderManager__pb2.StringMessage.SerializeToString,
            orderManager__pb2.Order.FromString,
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
    def searchOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/orderManager.OrderManagerService/searchOrders',
            orderManager__pb2.StringMessage.SerializeToString,
            orderManager__pb2.Order.FromString,
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
    def processOrders(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/orderManager.OrderManagerService/processOrders',
            orderManager__pb2.Order.SerializeToString,
            orderManager__pb2.CombinedShipment.FromString,
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
    def cancelShipment(request,
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
            '/orderManager.OrderManagerService/cancelShipment',
            orderManager__pb2.StringMessage.SerializeToString,
            orderManager__pb2.StringMessage.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
