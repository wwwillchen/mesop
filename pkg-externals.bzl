load("//:packages.bzl", "MDC_PACKAGES")

# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/cdk/config.bzl

# List of all entry-points of the Angular CDK package.
CDK_ENTRYPOINTS = [
    "a11y",
    "accordion",
    "bidi",
    "clipboard",
    "coercion",
    "collections",
    "dialog",
    "drag-drop",
    "keycodes",
    "layout",
    "listbox",
    "menu",
    "observers",
    "observers/private",
    "overlay",
    "platform",
    "portal",
    "scrolling",
    "stepper",
    "table",
    "text-field",
    "tree",
    "testing",
    "testing/testbed",
    "testing/selenium-webdriver",
]

# List of all entry-point targets of the Angular Material package.
CDK_TARGETS = ["//src/cdk"] + ["//src/cdk/%s" % ep for ep in CDK_ENTRYPOINTS]

# Within the CDK, only a few targets have sass libraries which need to be
# part of the release package. This list declares all CDK targets with sass
# libraries that need to be included and re-exported at the package root.
# **Note**: When updating the list of CDK entry-points with styles, also update
# the `exports` field in the `cdk/package.json` file.
CDK_ENTRYPOINTS_WITH_STYLES = [
    "a11y",
    "overlay",
    "text-field",
]

CDK_SCSS_LIBS = [
    "//src/cdk/%s:%s_scss_lib" % (p, p.replace("-", "_"))
    for p in CDK_ENTRYPOINTS_WITH_STYLES
]

# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/cdk-experimental/config.bzl

# List of all entry-points of the Angular cdk-experimental package.
CDK_EXPERIMENTAL_ENTRYPOINTS = [
    "column-resize",
    "combobox",
    "popover-edit",
    "scrolling",
    "selection",
    "table-scroll-container",
]

# Forked from:  https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/material/config.bzl

entryPoints = [
    "autocomplete",
    "autocomplete/testing",
    "badge",
    "badge/testing",
    "bottom-sheet",
    "bottom-sheet/testing",
    "button",
    "button/testing",
    "button-toggle",
    "button-toggle/testing",
    "card",
    "card/testing",
    "checkbox",
    "checkbox/testing",
    "chips",
    "chips/testing",
    "core",
    "core/testing",
    "datepicker",
    "datepicker/testing",
    "dialog",
    "dialog/testing",
    "divider",
    "divider/testing",
    "expansion",
    "expansion/testing",
    "form-field",
    "form-field/testing",
    "form-field/testing/control",
    "grid-list",
    "grid-list/testing",
    "icon",
    "icon/testing",
    "input",
    "input/testing",
    "list",
    "list/testing",
    "menu",
    "menu/testing",
    "paginator",
    "paginator/testing",
    "progress-bar",
    "progress-bar/testing",
    "progress-spinner",
    "progress-spinner/testing",
    "radio",
    "radio/testing",
    "select",
    "select/testing",
    "sidenav",
    "sidenav/testing",
    "slide-toggle",
    "slide-toggle/testing",
    "slider",
    "slider/testing",
    "snack-bar",
    "snack-bar/testing",
    "sort",
    "sort/testing",
    "stepper",
    "stepper/testing",
    "table",
    "table/testing",
    "tabs",
    "tabs/testing",
    "toolbar",
    "toolbar/testing",
    "tooltip",
    "tooltip/testing",
    "tree",
    "tree/testing",
]

# List of all non-testing entry-points of the Angular Material package.
MATERIAL_ENTRYPOINTS = [
    ep
    for ep in entryPoints
    if not "/testing" in ep
]

# List of all testing entry-points of the Angular Material package.
MATERIAL_TESTING_ENTRYPOINTS = [
    ep
    for ep in entryPoints
    if not ep in MATERIAL_ENTRYPOINTS
]

# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/material-experimental/config.bzl

experimental_entryPoints = [
    "column-resize",
    "menubar",
    "popover-edit",
    "selection",
]

# List of all non-testing entry-points of the Angular material-experimental package.
MATERIAL_EXPERIMENTAL_ENTRYPOINTS = [
    ep
    for ep in experimental_entryPoints
    if not "/testing" in ep
]

# List of all testing entry-points of the Angular material-experimental package.
MATERIAL_EXPERIMENTAL_TESTING_ENTRYPOINTS = [
    ep
    for ep in experimental_entryPoints
    if not ep in MATERIAL_EXPERIMENTAL_ENTRYPOINTS
]

# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/pkg-externals.bzl

# Base list of externals which should not be bundled into the APF package output.
# Note that we want to disable sorting of the externals as we manually group entries.
# buildifier: disable=unsorted-list-items
PKG_EXTERNALS = [
    # Framework packages.
    "@angular/animations",
    "@angular/common",
    "@angular/common/http",
    "@angular/common/http/testing",
    "@angular/common/testing",
    "@angular/core",
    "@angular/core/testing",
    "@angular/forms",
    "@angular/platform-browser",
    "@angular/platform-browser-dynamic",
    "@angular/platform-browser-dynamic/testing",
    "@angular/platform-browser/animations",
    "@angular/platform-server",
    "@angular/router",

    # Primary entry-points in the project.
    "@angular/cdk",
    "@angular/cdk-experimental",
    "@angular/google-maps",
    "@angular/material",
    "@angular/material-experimental",
    "@angular/material-moment-adapter",
    "@angular/material-luxon-adapter",
    "@angular/material-date-fns-adapter",
    "@angular/youtube-player",

    # Third-party libraries.
    "kagekiri",
    "moment",
    "moment/locale/fr",
    "moment/locale/ja",
    "luxon",
    "date-fns",
    "protractor",
    "rxjs",
    "rxjs/operators",
    "selenium-webdriver",

    # TODO: Remove slider deep dependencies after we remove depencies on MDC's javascript
    "@material/slider/adapter",
    "@material/slider/foundation",
    "@material/slider/types",
]

# Configures the externals for all MDC packages.
def setup_mdc_externals():
    for pkg_name in MDC_PACKAGES:
        PKG_EXTERNALS.append(pkg_name)

# Creates externals for a given package and its entry-points.
def setup_entry_point_externals(packageName, entryPoints):
    PKG_EXTERNALS.extend(["@angular/%s/%s" % (packageName, ep) for ep in entryPoints])

setup_mdc_externals()

setup_entry_point_externals("cdk", CDK_ENTRYPOINTS)
setup_entry_point_externals("cdk-experimental", CDK_EXPERIMENTAL_ENTRYPOINTS)
setup_entry_point_externals("material", MATERIAL_ENTRYPOINTS + MATERIAL_TESTING_ENTRYPOINTS)
setup_entry_point_externals(
    "material-experimental",
    MATERIAL_EXPERIMENTAL_ENTRYPOINTS + MATERIAL_EXPERIMENTAL_TESTING_ENTRYPOINTS,
)

# External module names in the examples package. Individual examples are grouped
# by package and component, so we add configure such entry-points as external.
setup_entry_point_externals("components-examples/cdk", CDK_ENTRYPOINTS)
setup_entry_point_externals("components-examples/cdk-experimental", CDK_EXPERIMENTAL_ENTRYPOINTS)
setup_entry_point_externals(
    "components-examples/material",
    MATERIAL_ENTRYPOINTS + MATERIAL_TESTING_ENTRYPOINTS,
)
setup_entry_point_externals(
    "components-examples/material-experimental",
    MATERIAL_EXPERIMENTAL_ENTRYPOINTS + MATERIAL_EXPERIMENTAL_TESTING_ENTRYPOINTS,
)
