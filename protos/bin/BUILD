load("@my_deps//:requirements.bzl", "requirement")
load("//builddefs:defs.bzl", "py_binary")
load("@aspect_rules_js//js:defs.bzl", "js_binary")

py_binary(
    name = "protoc_gen_mypy",
    srcs = ["protoc_gen_mypy_wrapper.py"],
    main = "protoc_gen_mypy_wrapper.py",
    visibility = ["//visibility:public"],
    deps = [
        requirement("mypy-protobuf"),
    ],
)

js_binary(
    name = "protoc_gen_es",
    copy_data_to_bin = False,
    data = ["@npm//@bufbuild/protoc-gen-es"],
    entry_point = ":protoc-gen-es",
    visibility = ["//visibility:public"],
)
