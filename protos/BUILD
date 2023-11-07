load("@rules_python//python:defs.bzl", "py_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@aspect_rules_ts//ts:proto.bzl", "ts_proto_library")
load("//builddefs:protos.bzl", "py_proto_library")

package(
    default_visibility = ["//visibility:public"],
)

proto_library(
    name = "ui_proto",
    srcs = ["ui.proto"],
)

py_proto_library(
    name = "ui_py_proto",
    srcs = ["ui.proto"],
)

ts_proto_library(
    # name of resulting ts_proto_library target
    name = "ui_ts_proto",
    # Label pointing to the linked node_modules target where @bufbuild/protoc-gen-es is linked, e.g
    node_modules = "//:node_modules",
    proto = ":ui_proto",
)
