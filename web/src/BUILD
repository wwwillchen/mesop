load("@build_bazel_rules_nodejs//:index.bzl", "pkg_web")
load("//tools:defaults.bzl", "devmode_esbuild", "esbuild_config", "http_server", "ng_module", "sass_binary")
load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")
load("@npm//@bazel/concatjs:index.bzl", "ts_config")

package(
    default_visibility = [":internal"],
)

package_group(
    name = "internal",
    packages = [
        "//...",
    ],
)

ts_config(
    name = "tsconfig-test",
    src = "bazel-tsconfig-test.json",
    deps = ["bazel-tsconfig-build.json"],
)

ng_module(
    name = "dev_app",
    srcs = [
        "dev_app.ts",
    ],
    deps = [
        "@npm//@angular/compiler",
    ],
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

devmode_esbuild(
    name = "bundles",
    config = ":esbuild_config",
    entry_points = [":main.ts"],
    platform = "browser",
    splitting = True,
    # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
    # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
    target = "es2016",
    # Note: We add all linker-processed FW packages as dependencies here so that ESBuild will
    # map all framework packages to their linker-processed bundles from `tools/angular`.
    deps = LINKER_PROCESSED_FW_PACKAGES + [
        ":dev_app",
    ],
)

# sass_binary(
#     name = "theme",
#     src = "theme.scss",
#     deps = [
#         "//src/material:sass_lib",
#         "//src/material-experimental:sass_lib",
#         "//src/material/core:theming_scss_lib",
#     ],
# )

# sass_binary(
#     name = "theme_m3",
#     src = "theme-m3.scss",
#     deps = [
#         "//src/material:sass_lib",
#         "//src/material-experimental:sass_lib",
#         "//src/material/core:theming_scss_lib",
#     ],
# )

# Variables that are going to be inlined into the dev app index.html.
filegroup(
    name = "variables",
    # Note that we need the * in the pattern, because there's a lint rule which
    # doesn't allow single files in a `glob`. We have to use a glob, because the file is optional.
    srcs = glob(["*variables.json"]),
)

# File group for all static files which are needed to serve the app. These files are
# used in the devserver as runfiles and will be copied into the static web package that can
# be deployed on static hosting services (like firebase).
filegroup(
    name = "dev_app_static_files",
    srcs = [
        "favicon.ico",
        "index.html",
        # ":theme",
        # ":theme_m3",
        ":variables",
        "@npm//:node_modules/moment/min/moment-with-locales.min.js",
        "@npm//:node_modules/rxjs/bundles/rxjs.umd.min.js",
        "@npm//:node_modules/zone.js/dist/zone.js",
    ],
)

http_server(
    name = "devserver",
    srcs = [":dev_app_static_files"],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for compatibility with "pkg_web" which always uses the tree
        # artifact output as workspace root.
        "angular_material",
    ],
    enable_dev_ui = True,
    tags = ["manual"],
    deps = [
        ":bundles",
    ],
)

# Target that builds a static web package of the app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":bundles",
        ":dev_app_static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
    ],
    tags = ["manual"],
)
