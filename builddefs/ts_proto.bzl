# Forked from: https://github.com/aspect-build/rules_ts/blob/9ad8eda1fcf25b4a83cb0c206832d8c3ff7e00d6/ts/proto.bzl

"""# Protocol Buffers and gRPC (UNSTABLE)

**UNSTABLE API**: contents of this page are not subject to our usual semver guarantees.
We may make breaking changes in any release.
Please try this API and provide feedback.
We intend to promote it to a stable API in a minor release, possibly as soon as v2.1.0.

`ts_proto_library` uses the Connect library from bufbuild, and supports both Web and Node.js:

- https://connectrpc.com/docs/web/getting-started
- https://connectrpc.com/docs/node/getting-started

This Bazel integration follows the "Local Generation" mechanism described at
https://connectrpc.com/docs/web/generating-code#local-generation,
using the `@bufbuild/protoc-gen-connect-es` and `@bufbuild/protoc-gen-es` packages as plugins to protoc.

The [aspect configure](https://docs.aspect.build/v/cli/commands/aspect_configure) command
auto-generates `ts_proto_library` rules as of the 5.7.2 release.
It's also possible to compile this library into your Gazelle binary.

Note: this API surface is not included in `defs.bzl` to avoid eager loads of rules_proto for all rules_ts users.

Installation
------------

If you install rules_ts in `WORKSPACE`, you'll need to install the deps of rules_proto, like this:

```
load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies")

rules_proto_dependencies()
```

If you use bzlmod/`MODULE.bazel` then no extra install is required.

Future work
-----------

- Allow users to choose other plugins. We intend to wait until http://github.com/bazelbuild/rules_proto supports protoc plugins.
- Allow users to control the output format. Currently it is hard-coded to `js+dts`, and the JS output uses ES Modules.
"""

load("@aspect_bazel_lib//lib:copy_to_directory.bzl", "copy_to_directory")
load("@aspect_bazel_lib//lib:directory_path.bzl", "directory_path", "make_directory_path")
load("@aspect_bazel_lib//lib:write_source_files.bzl", "write_source_files")
load("@aspect_rules_js//js:libs.bzl", "js_lib_helpers")
load("@aspect_rules_js//js:providers.bzl", "JsInfo", "js_info")
load("@rules_proto//proto:defs.bzl", "ProtoInfo", "proto_common")

def ts_proto_library(name, has_services = True, copy_files = True, files_to_copy = None, **kwargs):
    """
    A macro to generate JavaScript code and TypeScript typings from .proto files.

    Args:
        name: name of resulting ts_proto_library target
        has_services: whether the proto file contains a service, and therefore *_connect.{js,d.ts} should be written.
        copy_files: whether to copy the resulting .d.ts files back to the source tree, for the editor to locate them.
        files_to_copy: which files from the protoc output to copy. By default, scans for *.proto in the current package
            and replaces with the typical output filenames.
        **kwargs: additional named arguments to the ts_proto_library rule
    """
    protoc_gen_es_target = "_{}.gen_es".format(name)
    # protoc_gen_es_entry = protoc_gen_es_target + "__entry_point"

    # Output group name for the package directory of a linked package
    # package_directory_output_group = "package_directory"

    # native.filegroup(
    #     name = "dir",
    #     srcs = ["//node_modules/@bufbuild/protoc-gen-es"],
    #     output_group = package_directory_output_group,
    #     # tags = tags,
    #     # visibility = visibility,
    # )

    # # Reach into the node_modules to find the entry points
    # directory_path(
    #     name = protoc_gen_es_entry,
    #     tags = ["manual"],
    #     directory = ":dir",
    #     path = "bin/protoc-gen-es",
    # )

    protoc_gen_connect_es_target = None

    # js_binary(
    #     name = protoc_gen_es_target,
    #     data = ["@npm//@bufbuild/protoc-gen-es"],
    #     entry_point = "@npm//:node_modules/@bufbuild/protoc-gen-es/bin/protoc-gen-es",
    # )

    ts_proto_library_rule(
        name = name,
        protoc_gen_es = "//protos/bin:protoc_gen_es",
        protoc_gen_connect_es = protoc_gen_connect_es_target,
        # The codegen always has a runtime dependency on the protobuf runtime
        deps = kwargs.pop("deps", []) + ["@npm//@bufbuild/protobuf"],
        has_services = has_services,
        **kwargs
    )

    if not copy_files:
        return
    if not files_to_copy:
        proto_srcs = native.glob(["**/*.proto"])
        files_to_copy = [s.replace(".proto", "_pb.d.ts") for s in proto_srcs]

    files_target = "_{}.filegroup".format(name)
    dir_target = "_{}.directory".format(name)
    copy_target = "{}.copy".format(name)

    native.filegroup(
        name = files_target,
        srcs = [name],
        output_group = "types",
    )

    copy_to_directory(
        name = dir_target,
        srcs = [files_target],
        root_paths = ["**"],
    )

    write_source_files(
        name = copy_target,
        files = {
            f: make_directory_path("_{}_dirpath".format(f), dir_target, f)
            for f in files_to_copy
        },
    )

# Forked from: https://github.com/aspect-build/rules_ts/blob/9ad8eda1fcf25b4a83cb0c206832d8c3ff7e00d6/ts/private/ts_proto_library.bzl
"Private implementation details for ts_proto_library"

# buildifier: disable=function-docstring-header
def _protoc_action(ctx, proto_info, outputs, options = {
    "keep_empty_files": True,
    "target": "js+dts",
}):
    """Create an action like
    bazel-out/k8-opt-exec-2B5CBBC6/bin/external/com_google_protobuf/protoc $@' '' \
      '--plugin=protoc-gen-es=bazel-out/k8-opt-exec-2B5CBBC6/bin/plugin/bufbuild/protoc-gen-es.sh' \
      '--es_opt=keep_empty_files=true' '--es_opt=target=ts' \
      '--es_out=bazel-out/k8-fastbuild/bin' \
      '--descriptor_set_in=bazel-out/k8-fastbuild/bin/external/com_google_protobuf/timestamp_proto-descriptor-set.proto.bin:bazel-out/k8-fastbuild/bin/example/thing/thing_proto-descriptor-set.proto.bin:bazel-out/k8-fastbuild/bin/example/place/place_proto-descriptor-set.proto.bin:bazel-out/k8-fastbuild/bin/example/person/person_proto-descriptor-set.proto.bin' \
      example/person/person.proto
    """
    inputs = depset(proto_info.direct_sources, transitive = [proto_info.transitive_descriptor_sets])

    args = ctx.actions.args()
    args.add_joined(["--plugin", "protoc-gen-es", ctx.executable.protoc_gen_es.path], join_with = "=")
    for (key, value) in options.items():
        args.add_joined(["--es_opt", key, value], join_with = "=")
    args.add_joined(["--es_out", ctx.bin_dir.path], join_with = "=")

    if ctx.attr.has_services:
        args.add_joined(["--plugin", "protoc-gen-connect-es", ctx.executable.protoc_gen_connect_es.path], join_with = "=")
        for (key, value) in options.items():
            args.add_joined(["--connect-es_opt", key, value], join_with = "=")
        args.add_joined(["--connect-es_out", ctx.bin_dir.path], join_with = "=")

    args.add("--descriptor_set_in")
    args.add_joined(proto_info.transitive_descriptor_sets, join_with = ":")

    args.add_all(proto_info.direct_sources)

    ctx.actions.run(
        executable = ctx.executable.protoc,
        progress_message = "Generating .js/.d.ts from %{label}",
        outputs = outputs,
        inputs = inputs,
        arguments = [args],
        tools = [ctx.executable.protoc_gen_es] + (
            [ctx.executable.protoc_gen_connect_es] if ctx.attr.has_services else []
        ),
        env = {"BAZEL_BINDIR": ctx.bin_dir.path},
    )

def _declare_outs(ctx, info, ext):
    outs = proto_common.declare_generated_files(ctx.actions, info, "_pb" + ext)
    if ctx.attr.has_services:
        outs.extend(proto_common.declare_generated_files(ctx.actions, info, "_connect" + ext))
    return outs

def _ts_proto_library_impl(ctx):
    info = ctx.attr.proto[ProtoInfo]
    js_outs = _declare_outs(ctx, info, ".js")
    dts_outs = _declare_outs(ctx, info, ".d.ts")

    _protoc_action(ctx, info, js_outs + dts_outs)

    direct_srcs = depset(js_outs)
    direct_decls = depset(dts_outs)

    return [
        DefaultInfo(
            files = direct_srcs,
            runfiles = js_lib_helpers.gather_runfiles(
                ctx = ctx,
                sources = direct_srcs,
                data = [],
                deps = ctx.attr.deps,
            ),
        ),
        OutputGroupInfo(types = direct_decls),
        js_info(
            declarations = direct_decls,
            sources = direct_srcs,
            transitive_declarations = js_lib_helpers.gather_transitive_declarations(
                declarations = dts_outs,
                targets = ctx.attr.deps,
            ),
            transitive_sources = js_lib_helpers.gather_transitive_sources(
                sources = js_outs,
                targets = ctx.attr.deps,
            ),
        ),
    ]

ts_proto_library_rule = rule(
    implementation = _ts_proto_library_impl,
    attrs = {
        "deps": attr.label_list(
            providers = [JsInfo],
            doc = "Other ts_proto_library rules. TODO: could we collect them with an aspect",
        ),
        "has_services": attr.bool(
            doc = "whether to generate service stubs with gen-connect-es",
            default = True,
        ),
        "proto": attr.label(
            doc = "proto_library to generate JS/DTS for",
            providers = [ProtoInfo],
            mandatory = True,
        ),
        "protoc": attr.label(default = "@com_google_protobuf//:protoc", executable = True, cfg = "exec"),
        "protoc_gen_es": attr.label(
            doc = "protoc plugin to generate messages",
            mandatory = True,
            executable = True,
            cfg = "exec",
        ),
        "protoc_gen_connect_es": attr.label(
            doc = "protoc plugin to generate services",
            executable = True,
            cfg = "exec",
        ),
    },
)
