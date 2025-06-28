package magazzino.grpc;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
// @javax.annotation.Generated(
//     value = "by gRPC proto compiler (version 1.73.0)",
//     comments = "Source: magazzino.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class MagazzinoServiceGrpc {

  private MagazzinoServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "magazzino.grpc.MagazzinoService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<magazzino.grpc.Articolo,
      magazzino.grpc.StringMessage> getDepositaMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "deposita",
      requestType = magazzino.grpc.Articolo.class,
      responseType = magazzino.grpc.StringMessage.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<magazzino.grpc.Articolo,
      magazzino.grpc.StringMessage> getDepositaMethod() {
    io.grpc.MethodDescriptor<magazzino.grpc.Articolo, magazzino.grpc.StringMessage> getDepositaMethod;
    if ((getDepositaMethod = MagazzinoServiceGrpc.getDepositaMethod) == null) {
      synchronized (MagazzinoServiceGrpc.class) {
        if ((getDepositaMethod = MagazzinoServiceGrpc.getDepositaMethod) == null) {
          MagazzinoServiceGrpc.getDepositaMethod = getDepositaMethod =
              io.grpc.MethodDescriptor.<magazzino.grpc.Articolo, magazzino.grpc.StringMessage>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "deposita"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  magazzino.grpc.Articolo.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  magazzino.grpc.StringMessage.getDefaultInstance()))
              .setSchemaDescriptor(new MagazzinoServiceMethodDescriptorSupplier("deposita"))
              .build();
        }
      }
    }
    return getDepositaMethod;
  }

  private static volatile io.grpc.MethodDescriptor<magazzino.grpc.Empty,
      magazzino.grpc.Articolo> getPrelevaMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "preleva",
      requestType = magazzino.grpc.Empty.class,
      responseType = magazzino.grpc.Articolo.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<magazzino.grpc.Empty,
      magazzino.grpc.Articolo> getPrelevaMethod() {
    io.grpc.MethodDescriptor<magazzino.grpc.Empty, magazzino.grpc.Articolo> getPrelevaMethod;
    if ((getPrelevaMethod = MagazzinoServiceGrpc.getPrelevaMethod) == null) {
      synchronized (MagazzinoServiceGrpc.class) {
        if ((getPrelevaMethod = MagazzinoServiceGrpc.getPrelevaMethod) == null) {
          MagazzinoServiceGrpc.getPrelevaMethod = getPrelevaMethod =
              io.grpc.MethodDescriptor.<magazzino.grpc.Empty, magazzino.grpc.Articolo>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "preleva"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  magazzino.grpc.Empty.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  magazzino.grpc.Articolo.getDefaultInstance()))
              .setSchemaDescriptor(new MagazzinoServiceMethodDescriptorSupplier("preleva"))
              .build();
        }
      }
    }
    return getPrelevaMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static MagazzinoServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceStub>() {
        @java.lang.Override
        public MagazzinoServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MagazzinoServiceStub(channel, callOptions);
        }
      };
    return MagazzinoServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static MagazzinoServiceBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceBlockingV2Stub>() {
        @java.lang.Override
        public MagazzinoServiceBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MagazzinoServiceBlockingV2Stub(channel, callOptions);
        }
      };
    return MagazzinoServiceBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static MagazzinoServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceBlockingStub>() {
        @java.lang.Override
        public MagazzinoServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MagazzinoServiceBlockingStub(channel, callOptions);
        }
      };
    return MagazzinoServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static MagazzinoServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<MagazzinoServiceFutureStub>() {
        @java.lang.Override
        public MagazzinoServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new MagazzinoServiceFutureStub(channel, callOptions);
        }
      };
    return MagazzinoServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void deposita(magazzino.grpc.Articolo request,
        io.grpc.stub.StreamObserver<magazzino.grpc.StringMessage> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getDepositaMethod(), responseObserver);
    }

    /**
     */
    default void preleva(magazzino.grpc.Empty request,
        io.grpc.stub.StreamObserver<magazzino.grpc.Articolo> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getPrelevaMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service MagazzinoService.
   */
  public static abstract class MagazzinoServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return MagazzinoServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service MagazzinoService.
   */
  public static final class MagazzinoServiceStub
      extends io.grpc.stub.AbstractAsyncStub<MagazzinoServiceStub> {
    private MagazzinoServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MagazzinoServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MagazzinoServiceStub(channel, callOptions);
    }

    /**
     */
    public void deposita(magazzino.grpc.Articolo request,
        io.grpc.stub.StreamObserver<magazzino.grpc.StringMessage> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getDepositaMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void preleva(magazzino.grpc.Empty request,
        io.grpc.stub.StreamObserver<magazzino.grpc.Articolo> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getPrelevaMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service MagazzinoService.
   */
  public static final class MagazzinoServiceBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<MagazzinoServiceBlockingV2Stub> {
    private MagazzinoServiceBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MagazzinoServiceBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MagazzinoServiceBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public magazzino.grpc.StringMessage deposita(magazzino.grpc.Articolo request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDepositaMethod(), getCallOptions(), request);
    }

    /**
     */
    public magazzino.grpc.Articolo preleva(magazzino.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPrelevaMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service MagazzinoService.
   */
  public static final class MagazzinoServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<MagazzinoServiceBlockingStub> {
    private MagazzinoServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MagazzinoServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MagazzinoServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public magazzino.grpc.StringMessage deposita(magazzino.grpc.Articolo request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getDepositaMethod(), getCallOptions(), request);
    }

    /**
     */
    public magazzino.grpc.Articolo preleva(magazzino.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getPrelevaMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service MagazzinoService.
   */
  public static final class MagazzinoServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<MagazzinoServiceFutureStub> {
    private MagazzinoServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected MagazzinoServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new MagazzinoServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<magazzino.grpc.StringMessage> deposita(
        magazzino.grpc.Articolo request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getDepositaMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<magazzino.grpc.Articolo> preleva(
        magazzino.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getPrelevaMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_DEPOSITA = 0;
  private static final int METHODID_PRELEVA = 1;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_DEPOSITA:
          serviceImpl.deposita((magazzino.grpc.Articolo) request,
              (io.grpc.stub.StreamObserver<magazzino.grpc.StringMessage>) responseObserver);
          break;
        case METHODID_PRELEVA:
          serviceImpl.preleva((magazzino.grpc.Empty) request,
              (io.grpc.stub.StreamObserver<magazzino.grpc.Articolo>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getDepositaMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              magazzino.grpc.Articolo,
              magazzino.grpc.StringMessage>(
                service, METHODID_DEPOSITA)))
        .addMethod(
          getPrelevaMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              magazzino.grpc.Empty,
              magazzino.grpc.Articolo>(
                service, METHODID_PRELEVA)))
        .build();
  }

  private static abstract class MagazzinoServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    MagazzinoServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return magazzino.grpc.Magazzino.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("MagazzinoService");
    }
  }

  private static final class MagazzinoServiceFileDescriptorSupplier
      extends MagazzinoServiceBaseDescriptorSupplier {
    MagazzinoServiceFileDescriptorSupplier() {}
  }

  private static final class MagazzinoServiceMethodDescriptorSupplier
      extends MagazzinoServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    MagazzinoServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (MagazzinoServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new MagazzinoServiceFileDescriptorSupplier())
              .addMethod(getDepositaMethod())
              .addMethod(getPrelevaMethod())
              .build();
        }
      }
    }
    return result;
  }
}
