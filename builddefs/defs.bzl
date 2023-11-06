# Wrapper for commonly used Bazel rules.

load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("//tools:defaults.bzl", _ts_library = "ts_library")

py_binary = _py_binary
py_library = _py_library

ts_library = _ts_library
