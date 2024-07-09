# frozen_string_literal: true
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/compiler/plugin.proto

require 'google/protobuf'

require 'google/protobuf/descriptor_pb'


descriptor_data = "\n%google/protobuf/compiler/plugin.proto\x12\x18google.protobuf.compiler\x1a google/protobuf/descriptor.proto\"F\n\x07Version\x12\r\n\x05major\x18\x01 \x01(\x05\x12\r\n\x05minor\x18\x02 \x01(\x05\x12\r\n\x05patch\x18\x03 \x01(\x05\x12\x0e\n\x06suffix\x18\x04 \x01(\t\"\x81\x02\n\x14\x43odeGeneratorRequest\x12\x18\n\x10\x66ile_to_generate\x18\x01 \x03(\t\x12\x11\n\tparameter\x18\x02 \x01(\t\x12\x38\n\nproto_file\x18\x0f \x03(\x0b\x32$.google.protobuf.FileDescriptorProto\x12\x45\n\x17source_file_descriptors\x18\x11 \x03(\x0b\x32$.google.protobuf.FileDescriptorProto\x12;\n\x10\x63ompiler_version\x18\x03 \x01(\x0b\x32!.google.protobuf.compiler.Version\"\x92\x03\n\x15\x43odeGeneratorResponse\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x1a\n\x12supported_features\x18\x02 \x01(\x04\x12\x17\n\x0fminimum_edition\x18\x03 \x01(\x05\x12\x17\n\x0fmaximum_edition\x18\x04 \x01(\x05\x12\x42\n\x04\x66ile\x18\x0f \x03(\x0b\x32\x34.google.protobuf.compiler.CodeGeneratorResponse.File\x1a\x7f\n\x04\x46ile\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x17\n\x0finsertion_point\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x0f \x01(\t\x12?\n\x13generated_code_info\x18\x10 \x01(\x0b\x32\".google.protobuf.GeneratedCodeInfo\"W\n\x07\x46\x65\x61ture\x12\x10\n\x0c\x46\x45\x41TURE_NONE\x10\x00\x12\x1b\n\x17\x46\x45\x41TURE_PROTO3_OPTIONAL\x10\x01\x12\x1d\n\x19\x46\x45\x41TURE_SUPPORTS_EDITIONS\x10\x02\x42r\n\x1c\x63om.google.protobuf.compilerB\x0cPluginProtosZ)google.golang.org/protobuf/types/pluginpb\xaa\x02\x18Google.Protobuf.Compiler"

pool = Google::Protobuf::DescriptorPool.generated_pool
pool.add_serialized_file(descriptor_data)

module Google
  module Protobuf
    module Compiler
      Version = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("google.protobuf.compiler.Version").msgclass
      CodeGeneratorRequest = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("google.protobuf.compiler.CodeGeneratorRequest").msgclass
      CodeGeneratorResponse = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("google.protobuf.compiler.CodeGeneratorResponse").msgclass
      CodeGeneratorResponse::File = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("google.protobuf.compiler.CodeGeneratorResponse.File").msgclass
      CodeGeneratorResponse::Feature = ::Google::Protobuf::DescriptorPool.generated_pool.lookup("google.protobuf.compiler.CodeGeneratorResponse.Feature").enummodule
    end
  end
end