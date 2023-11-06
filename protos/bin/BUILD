load("@my_deps//:requirements.bzl", "requirement")
load("//builddefs:defs.bzl", "py_binary")
load("@bazel_skylib//rules:native_binary.bzl", "native_binary")

py_binary(
    name = "protoc_gen_mypy",
    srcs = ["protoc_gen_mypy_wrapper.py"],
    main = "protoc_gen_mypy_wrapper.py",
    visibility = ["//visibility:public"],
    deps = [
        requirement("mypy-protobuf"),
    ],
)

native_binary(
    name = "protoc_gen_ts",
    src = "//node_modules/.bin/protoc-gen-ts_proto",
    out = "protoc-gen-ts_proto",
    visibility = ["//visibility:public"],
)
