// Generated by the protocol buffer compiler.  DO NOT EDIT!
// NO CHECKED-IN PROTOBUF GENCODE
// source: magazzino.proto
// Protobuf Java Version: 4.31.1

package magazzinoExample.magazzino;

/**
 * Protobuf type {@code magazzinoExample.magazzino.Empty}
 */
@com.google.protobuf.Generated
public final class Empty extends
    com.google.protobuf.GeneratedMessage implements
    // @@protoc_insertion_point(message_implements:magazzinoExample.magazzino.Empty)
    EmptyOrBuilder {
private static final long serialVersionUID = 0L;
  static {
    com.google.protobuf.RuntimeVersion.validateProtobufGencodeVersion(
      com.google.protobuf.RuntimeVersion.RuntimeDomain.PUBLIC,
      /* major= */ 4,
      /* minor= */ 31,
      /* patch= */ 1,
      /* suffix= */ "",
      Empty.class.getName());
  }
  // Use Empty.newBuilder() to construct.
  private Empty(com.google.protobuf.GeneratedMessage.Builder<?> builder) {
    super(builder);
  }
  private Empty() {
  }

  public static final com.google.protobuf.Descriptors.Descriptor
      getDescriptor() {
    return magazzinoExample.magazzino.MagazzinoOuterClass.internal_static_magazzinoExample_magazzino_Empty_descriptor;
  }

  @java.lang.Override
  protected com.google.protobuf.GeneratedMessage.FieldAccessorTable
      internalGetFieldAccessorTable() {
    return magazzinoExample.magazzino.MagazzinoOuterClass.internal_static_magazzinoExample_magazzino_Empty_fieldAccessorTable
        .ensureFieldAccessorsInitialized(
            magazzinoExample.magazzino.Empty.class, magazzinoExample.magazzino.Empty.Builder.class);
  }

  private byte memoizedIsInitialized = -1;
  @java.lang.Override
  public final boolean isInitialized() {
    byte isInitialized = memoizedIsInitialized;
    if (isInitialized == 1) return true;
    if (isInitialized == 0) return false;

    memoizedIsInitialized = 1;
    return true;
  }

  @java.lang.Override
  public void writeTo(com.google.protobuf.CodedOutputStream output)
                      throws java.io.IOException {
    getUnknownFields().writeTo(output);
  }

  @java.lang.Override
  public int getSerializedSize() {
    int size = memoizedSize;
    if (size != -1) return size;

    size = 0;
    size += getUnknownFields().getSerializedSize();
    memoizedSize = size;
    return size;
  }

  @java.lang.Override
  public boolean equals(final java.lang.Object obj) {
    if (obj == this) {
     return true;
    }
    if (!(obj instanceof magazzinoExample.magazzino.Empty)) {
      return super.equals(obj);
    }
    magazzinoExample.magazzino.Empty other = (magazzinoExample.magazzino.Empty) obj;

    if (!getUnknownFields().equals(other.getUnknownFields())) return false;
    return true;
  }

  @java.lang.Override
  public int hashCode() {
    if (memoizedHashCode != 0) {
      return memoizedHashCode;
    }
    int hash = 41;
    hash = (19 * hash) + getDescriptor().hashCode();
    hash = (29 * hash) + getUnknownFields().hashCode();
    memoizedHashCode = hash;
    return hash;
  }

  public static magazzinoExample.magazzino.Empty parseFrom(
      java.nio.ByteBuffer data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      java.nio.ByteBuffer data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      com.google.protobuf.ByteString data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      com.google.protobuf.ByteString data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(byte[] data)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      byte[] data,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws com.google.protobuf.InvalidProtocolBufferException {
    return PARSER.parseFrom(data, extensionRegistry);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(java.io.InputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseWithIOException(PARSER, input);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      java.io.InputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseWithIOException(PARSER, input, extensionRegistry);
  }

  public static magazzinoExample.magazzino.Empty parseDelimitedFrom(java.io.InputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseDelimitedWithIOException(PARSER, input);
  }

  public static magazzinoExample.magazzino.Empty parseDelimitedFrom(
      java.io.InputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseDelimitedWithIOException(PARSER, input, extensionRegistry);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      com.google.protobuf.CodedInputStream input)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseWithIOException(PARSER, input);
  }
  public static magazzinoExample.magazzino.Empty parseFrom(
      com.google.protobuf.CodedInputStream input,
      com.google.protobuf.ExtensionRegistryLite extensionRegistry)
      throws java.io.IOException {
    return com.google.protobuf.GeneratedMessage
        .parseWithIOException(PARSER, input, extensionRegistry);
  }

  @java.lang.Override
  public Builder newBuilderForType() { return newBuilder(); }
  public static Builder newBuilder() {
    return DEFAULT_INSTANCE.toBuilder();
  }
  public static Builder newBuilder(magazzinoExample.magazzino.Empty prototype) {
    return DEFAULT_INSTANCE.toBuilder().mergeFrom(prototype);
  }
  @java.lang.Override
  public Builder toBuilder() {
    return this == DEFAULT_INSTANCE
        ? new Builder() : new Builder().mergeFrom(this);
  }

  @java.lang.Override
  protected Builder newBuilderForType(
      com.google.protobuf.GeneratedMessage.BuilderParent parent) {
    Builder builder = new Builder(parent);
    return builder;
  }
  /**
   * Protobuf type {@code magazzinoExample.magazzino.Empty}
   */
  public static final class Builder extends
      com.google.protobuf.GeneratedMessage.Builder<Builder> implements
      // @@protoc_insertion_point(builder_implements:magazzinoExample.magazzino.Empty)
      magazzinoExample.magazzino.EmptyOrBuilder {
    public static final com.google.protobuf.Descriptors.Descriptor
        getDescriptor() {
      return magazzinoExample.magazzino.MagazzinoOuterClass.internal_static_magazzinoExample_magazzino_Empty_descriptor;
    }

    @java.lang.Override
    protected com.google.protobuf.GeneratedMessage.FieldAccessorTable
        internalGetFieldAccessorTable() {
      return magazzinoExample.magazzino.MagazzinoOuterClass.internal_static_magazzinoExample_magazzino_Empty_fieldAccessorTable
          .ensureFieldAccessorsInitialized(
              magazzinoExample.magazzino.Empty.class, magazzinoExample.magazzino.Empty.Builder.class);
    }

    // Construct using magazzinoExample.magazzino.Empty.newBuilder()
    private Builder() {

    }

    private Builder(
        com.google.protobuf.GeneratedMessage.BuilderParent parent) {
      super(parent);

    }
    @java.lang.Override
    public Builder clear() {
      super.clear();
      return this;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.Descriptor
        getDescriptorForType() {
      return magazzinoExample.magazzino.MagazzinoOuterClass.internal_static_magazzinoExample_magazzino_Empty_descriptor;
    }

    @java.lang.Override
    public magazzinoExample.magazzino.Empty getDefaultInstanceForType() {
      return magazzinoExample.magazzino.Empty.getDefaultInstance();
    }

    @java.lang.Override
    public magazzinoExample.magazzino.Empty build() {
      magazzinoExample.magazzino.Empty result = buildPartial();
      if (!result.isInitialized()) {
        throw newUninitializedMessageException(result);
      }
      return result;
    }

    @java.lang.Override
    public magazzinoExample.magazzino.Empty buildPartial() {
      magazzinoExample.magazzino.Empty result = new magazzinoExample.magazzino.Empty(this);
      onBuilt();
      return result;
    }

    @java.lang.Override
    public Builder mergeFrom(com.google.protobuf.Message other) {
      if (other instanceof magazzinoExample.magazzino.Empty) {
        return mergeFrom((magazzinoExample.magazzino.Empty)other);
      } else {
        super.mergeFrom(other);
        return this;
      }
    }

    public Builder mergeFrom(magazzinoExample.magazzino.Empty other) {
      if (other == magazzinoExample.magazzino.Empty.getDefaultInstance()) return this;
      this.mergeUnknownFields(other.getUnknownFields());
      onChanged();
      return this;
    }

    @java.lang.Override
    public final boolean isInitialized() {
      return true;
    }

    @java.lang.Override
    public Builder mergeFrom(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws java.io.IOException {
      if (extensionRegistry == null) {
        throw new java.lang.NullPointerException();
      }
      try {
        boolean done = false;
        while (!done) {
          int tag = input.readTag();
          switch (tag) {
            case 0:
              done = true;
              break;
            default: {
              if (!super.parseUnknownField(input, extensionRegistry, tag)) {
                done = true; // was an endgroup tag
              }
              break;
            } // default:
          } // switch (tag)
        } // while (!done)
      } catch (com.google.protobuf.InvalidProtocolBufferException e) {
        throw e.unwrapIOException();
      } finally {
        onChanged();
      } // finally
      return this;
    }

    // @@protoc_insertion_point(builder_scope:magazzinoExample.magazzino.Empty)
  }

  // @@protoc_insertion_point(class_scope:magazzinoExample.magazzino.Empty)
  private static final magazzinoExample.magazzino.Empty DEFAULT_INSTANCE;
  static {
    DEFAULT_INSTANCE = new magazzinoExample.magazzino.Empty();
  }

  public static magazzinoExample.magazzino.Empty getDefaultInstance() {
    return DEFAULT_INSTANCE;
  }

  private static final com.google.protobuf.Parser<Empty>
      PARSER = new com.google.protobuf.AbstractParser<Empty>() {
    @java.lang.Override
    public Empty parsePartialFrom(
        com.google.protobuf.CodedInputStream input,
        com.google.protobuf.ExtensionRegistryLite extensionRegistry)
        throws com.google.protobuf.InvalidProtocolBufferException {
      Builder builder = newBuilder();
      try {
        builder.mergeFrom(input, extensionRegistry);
      } catch (com.google.protobuf.InvalidProtocolBufferException e) {
        throw e.setUnfinishedMessage(builder.buildPartial());
      } catch (com.google.protobuf.UninitializedMessageException e) {
        throw e.asInvalidProtocolBufferException().setUnfinishedMessage(builder.buildPartial());
      } catch (java.io.IOException e) {
        throw new com.google.protobuf.InvalidProtocolBufferException(e)
            .setUnfinishedMessage(builder.buildPartial());
      }
      return builder.buildPartial();
    }
  };

  public static com.google.protobuf.Parser<Empty> parser() {
    return PARSER;
  }

  @java.lang.Override
  public com.google.protobuf.Parser<Empty> getParserForType() {
    return PARSER;
  }

  @java.lang.Override
  public magazzinoExample.magazzino.Empty getDefaultInstanceForType() {
    return DEFAULT_INSTANCE;
  }

}

