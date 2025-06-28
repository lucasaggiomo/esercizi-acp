package laptopService.grpc;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
// @javax.annotation.Generated(
//     value = "by gRPC proto compiler (version 1.73.0)",
//     comments = "Source: laptopService.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class LaptopServiceGrpc {

  private LaptopServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "laptopService.grpc.LaptopService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<laptopService.grpc.Empty,
      laptopService.grpc.Laptop> getBuyMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "buy",
      requestType = laptopService.grpc.Empty.class,
      responseType = laptopService.grpc.Laptop.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<laptopService.grpc.Empty,
      laptopService.grpc.Laptop> getBuyMethod() {
    io.grpc.MethodDescriptor<laptopService.grpc.Empty, laptopService.grpc.Laptop> getBuyMethod;
    if ((getBuyMethod = LaptopServiceGrpc.getBuyMethod) == null) {
      synchronized (LaptopServiceGrpc.class) {
        if ((getBuyMethod = LaptopServiceGrpc.getBuyMethod) == null) {
          LaptopServiceGrpc.getBuyMethod = getBuyMethod =
              io.grpc.MethodDescriptor.<laptopService.grpc.Empty, laptopService.grpc.Laptop>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "buy"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  laptopService.grpc.Empty.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  laptopService.grpc.Laptop.getDefaultInstance()))
              .setSchemaDescriptor(new LaptopServiceMethodDescriptorSupplier("buy"))
              .build();
        }
      }
    }
    return getBuyMethod;
  }

  private static volatile io.grpc.MethodDescriptor<laptopService.grpc.Laptop,
      laptopService.grpc.StringMessage> getSellMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "sell",
      requestType = laptopService.grpc.Laptop.class,
      responseType = laptopService.grpc.StringMessage.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<laptopService.grpc.Laptop,
      laptopService.grpc.StringMessage> getSellMethod() {
    io.grpc.MethodDescriptor<laptopService.grpc.Laptop, laptopService.grpc.StringMessage> getSellMethod;
    if ((getSellMethod = LaptopServiceGrpc.getSellMethod) == null) {
      synchronized (LaptopServiceGrpc.class) {
        if ((getSellMethod = LaptopServiceGrpc.getSellMethod) == null) {
          LaptopServiceGrpc.getSellMethod = getSellMethod =
              io.grpc.MethodDescriptor.<laptopService.grpc.Laptop, laptopService.grpc.StringMessage>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "sell"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  laptopService.grpc.Laptop.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  laptopService.grpc.StringMessage.getDefaultInstance()))
              .setSchemaDescriptor(new LaptopServiceMethodDescriptorSupplier("sell"))
              .build();
        }
      }
    }
    return getSellMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static LaptopServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<LaptopServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<LaptopServiceStub>() {
        @java.lang.Override
        public LaptopServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new LaptopServiceStub(channel, callOptions);
        }
      };
    return LaptopServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static LaptopServiceBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<LaptopServiceBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<LaptopServiceBlockingV2Stub>() {
        @java.lang.Override
        public LaptopServiceBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new LaptopServiceBlockingV2Stub(channel, callOptions);
        }
      };
    return LaptopServiceBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static LaptopServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<LaptopServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<LaptopServiceBlockingStub>() {
        @java.lang.Override
        public LaptopServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new LaptopServiceBlockingStub(channel, callOptions);
        }
      };
    return LaptopServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static LaptopServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<LaptopServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<LaptopServiceFutureStub>() {
        @java.lang.Override
        public LaptopServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new LaptopServiceFutureStub(channel, callOptions);
        }
      };
    return LaptopServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void buy(laptopService.grpc.Empty request,
        io.grpc.stub.StreamObserver<laptopService.grpc.Laptop> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getBuyMethod(), responseObserver);
    }

    /**
     */
    default void sell(laptopService.grpc.Laptop request,
        io.grpc.stub.StreamObserver<laptopService.grpc.StringMessage> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getSellMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service LaptopService.
   */
  public static abstract class LaptopServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return LaptopServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service LaptopService.
   */
  public static final class LaptopServiceStub
      extends io.grpc.stub.AbstractAsyncStub<LaptopServiceStub> {
    private LaptopServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected LaptopServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new LaptopServiceStub(channel, callOptions);
    }

    /**
     */
    public void buy(laptopService.grpc.Empty request,
        io.grpc.stub.StreamObserver<laptopService.grpc.Laptop> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getBuyMethod(), getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void sell(laptopService.grpc.Laptop request,
        io.grpc.stub.StreamObserver<laptopService.grpc.StringMessage> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getSellMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service LaptopService.
   */
  public static final class LaptopServiceBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<LaptopServiceBlockingV2Stub> {
    private LaptopServiceBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected LaptopServiceBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new LaptopServiceBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public laptopService.grpc.Laptop buy(laptopService.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getBuyMethod(), getCallOptions(), request);
    }

    /**
     */
    public laptopService.grpc.StringMessage sell(laptopService.grpc.Laptop request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getSellMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service LaptopService.
   */
  public static final class LaptopServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<LaptopServiceBlockingStub> {
    private LaptopServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected LaptopServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new LaptopServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public laptopService.grpc.Laptop buy(laptopService.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getBuyMethod(), getCallOptions(), request);
    }

    /**
     */
    public laptopService.grpc.StringMessage sell(laptopService.grpc.Laptop request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getSellMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service LaptopService.
   */
  public static final class LaptopServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<LaptopServiceFutureStub> {
    private LaptopServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected LaptopServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new LaptopServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<laptopService.grpc.Laptop> buy(
        laptopService.grpc.Empty request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getBuyMethod(), getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<laptopService.grpc.StringMessage> sell(
        laptopService.grpc.Laptop request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getSellMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_BUY = 0;
  private static final int METHODID_SELL = 1;

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
        case METHODID_BUY:
          serviceImpl.buy((laptopService.grpc.Empty) request,
              (io.grpc.stub.StreamObserver<laptopService.grpc.Laptop>) responseObserver);
          break;
        case METHODID_SELL:
          serviceImpl.sell((laptopService.grpc.Laptop) request,
              (io.grpc.stub.StreamObserver<laptopService.grpc.StringMessage>) responseObserver);
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
          getBuyMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              laptopService.grpc.Empty,
              laptopService.grpc.Laptop>(
                service, METHODID_BUY)))
        .addMethod(
          getSellMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              laptopService.grpc.Laptop,
              laptopService.grpc.StringMessage>(
                service, METHODID_SELL)))
        .build();
  }

  private static abstract class LaptopServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    LaptopServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return laptopService.grpc.LaptopServiceOuterClass.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("LaptopService");
    }
  }

  private static final class LaptopServiceFileDescriptorSupplier
      extends LaptopServiceBaseDescriptorSupplier {
    LaptopServiceFileDescriptorSupplier() {}
  }

  private static final class LaptopServiceMethodDescriptorSupplier
      extends LaptopServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    LaptopServiceMethodDescriptorSupplier(java.lang.String methodName) {
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
      synchronized (LaptopServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new LaptopServiceFileDescriptorSupplier())
              .addMethod(getBuyMethod())
              .addMethod(getSellMethod())
              .build();
        }
      }
    }
    return result;
  }
}
