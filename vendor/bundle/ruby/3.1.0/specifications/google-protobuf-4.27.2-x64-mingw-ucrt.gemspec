# -*- encoding: utf-8 -*-
# stub: google-protobuf 4.27.2 x64-mingw-ucrt lib

Gem::Specification.new do |s|
  s.name = "google-protobuf".freeze
  s.version = "4.27.2"
  s.platform = "x64-mingw-ucrt".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "source_code_uri" => "https://github.com/protocolbuffers/protobuf/tree/v4.27.2/ruby" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Protobuf Authors".freeze]
  s.date = "2024-06-25"
  s.description = "Protocol Buffers are Google's data interchange format.".freeze
  s.email = "protobuf@googlegroups.com".freeze
  s.homepage = "https://developers.google.com/protocol-buffers".freeze
  s.licenses = ["BSD-3-Clause".freeze]
  s.required_ruby_version = Gem::Requirement.new([">= 3.1".freeze, "< 3.4.dev".freeze])
  s.rubygems_version = "3.3.7".freeze
  s.summary = "Protocol Buffers".freeze

  s.installed_by_version = "3.3.7" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_development_dependency(%q<rake-compiler-dock>.freeze, ["= 1.2.1"])
    s.add_runtime_dependency(%q<bigdecimal>.freeze, [">= 0"])
    s.add_runtime_dependency(%q<rake>.freeze, [">= 13"])
    s.add_development_dependency(%q<ffi>.freeze, ["~> 1"])
    s.add_development_dependency(%q<ffi-compiler>.freeze, ["~> 1"])
    s.add_development_dependency(%q<rake-compiler>.freeze, ["~> 1.1.0"])
    s.add_development_dependency(%q<test-unit>.freeze, ["~> 3.0", ">= 3.0.9"])
  else
    s.add_dependency(%q<rake-compiler-dock>.freeze, ["= 1.2.1"])
    s.add_dependency(%q<bigdecimal>.freeze, [">= 0"])
    s.add_dependency(%q<rake>.freeze, [">= 13"])
    s.add_dependency(%q<ffi>.freeze, ["~> 1"])
    s.add_dependency(%q<ffi-compiler>.freeze, ["~> 1"])
    s.add_dependency(%q<rake-compiler>.freeze, ["~> 1.1.0"])
    s.add_dependency(%q<test-unit>.freeze, ["~> 3.0", ">= 3.0.9"])
  end
end
