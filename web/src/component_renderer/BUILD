load("//tools:defaults.bzl", "ng_module")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "component_renderer",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        # INSERT COMPONENT IMPORTS HERE:
        "//optic/components/foo_bar:ng",
        "//optic/components/button:ng",
        "//optic/components/checkbox:ng",
        "//optic/components/text:ng",
        "//protos:ui_ts_proto",
        "@npm//@angular/compiler",
    ],
)
