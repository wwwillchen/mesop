load("@build_bazel_rules_nodejs//:index.bzl", "pkg_web")
load("//tools:defaults.bzl", "devmode_esbuild", "esbuild_config", "http_server", "ng_module", "sass_binary")
load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")

package(default_visibility = ["//visibility:public"])

ng_module(
    name = "will",
    srcs = [
        "will.ts",
    ],
    deps = [
        "@npm//@angular/compiler",
    ],
)
