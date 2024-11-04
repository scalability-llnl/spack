# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shutil
import sys
import tempfile

import llnl.util.tty as tty

from spack.operating_systems.mac_os import macos_version
from spack.package import *

MACOS_VERSION = macos_version() if sys.platform == "darwin" else None


class QtPackage(CMakePackage):
    """Base package for Qt6 components"""

    homepage = "https://www.qt.io"

    @staticmethod
    def get_url(qualname):
        _url = "https://github.com/qt/{}/archive/refs/tags/v6.2.3.tar.gz"
        return _url.format(qualname.lower())

    @staticmethod
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
        return _list_url.format(qualname.lower())

    maintainers("wdconinc")

    # Default dependencies for all qt-* components
    generator("ninja")
    depends_on("cmake@3.16:", type="build")
    depends_on("pkgconfig", type="build", when="platform=linux")
    depends_on("python", type="build")

    # List of unnecessary directories in src/3rdparty
    vendor_deps_to_remove = []

    @run_after("patch")
    def remove_vendor_deps(self, vendor_dir, vendor_deps_to_remove):
        """Remove src/3rdparty libraries that are provided by spack"""
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep in vendor_deps_to_remove:
                        shutil.rmtree(dep)

    def cmake_args(self):
        # Start with upstream cmake_args
        args = super().cmake_args()

        # Qt components typically install cmake config files in a single prefix,
        # so we have to point them to the cmake config files of dependencies
        qt_prefix_path = []
        re_qt = re.compile("qt-.*")
        for dep in self.spec.dependencies():
            if re_qt.match(dep.name):
                qt_prefix_path.append(self.spec[dep.name].prefix)

        # Now append all qt-* dependency prefixex into a prefix path
        args.append(self.define("QT_ADDITIONAL_PACKAGES_PREFIX_PATH", ":".join(qt_prefix_path)))

        return args

    @run_after("install")
    def install_config_summary(self):
        """Copy the config.summary into the prefix"""

        # Copy to package-name-prefixed file to avoid clashes in views
        with working_dir(self.build_directory):
            copy("config.summary", self.name + ".config.summary")
            install(self.name + ".config.summary", self.prefix)

        # Warn users that this config summary is only for info purpose,
        # and should not be relied upon for downstream parsing.
        tty.warn("config.summary in prefix is a temporary feature only")

    @run_after("install")
    def add_qt_module_files(self):
        """Qt modules need to drop a forwarding qt_module.pri file in the qt-base
        mkspecs/modules directory. This violates the spack install prefix separation,
        so we modify the downstream module files to work regardless."""

        # No need to modify qt-base itself
        if self.spec.name == "qt-base":
            return

        # Define qt_module.pri filename, but postpone writing until after loop
        qt_module_pri = join_path(self.prefix.mkspecs.modules, "qt_module.pri")

        # Include qt_module.pri file in every pri file
        for old_file in find(self.prefix.mkspecs.modules, "*.pri"):
            new_fd, new_file = tempfile.mkstemp(
                prefix=os.path.basename(old_file), dir=self.prefix.mkspecs.modules
            )
            with os.fdopen(new_fd, "w") as new_fh:
                new_fh.write("include(qt_module.pri)\n")
                with open(old_file, "r") as old_fh:
                    new_fh.write(old_fh.read())
            shutil.move(new_file, old_file)

        # Create qt_module.pri file with definitions
        defs = []
        for dir in ["BIN", "INCLUDE", "LIB"]:
            if os.path.exists(join_path(self.prefix, dir.lower())):
                defs.append(f"QT_MODULE_{dir}_BASE = {join_path(self.prefix, dir.lower())}\n")
        with open(qt_module_pri, "w") as file:
            file.write("\n".join(defs))

    def setup_run_environment(self, env):
        env.prepend_path("QMAKEPATH", self.prefix)
        if os.path.exists(self.prefix.mkspecs.modules):
            env.prepend_path("QMAKE_MODULE_PATH", self.prefix.mkspecs.modules)
        if os.path.exists(self.prefix.plugins):
            env.prepend_path("QT_PLUGIN_PATH", self.prefix.plugins)


class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)

    provides("qmake")

    license("BSD-3-Clause")

    version("6.7.3", sha256="65771d1618cab08ec5e9bbfdc265b5d2ce2ccf0373143d7d9d139647a7196aec")
    version("6.7.2", sha256="96b96e4fd0fc306502ed8b94a34cfa0bacc8a25d43c2e958dd6772b28f6b0e42")
    version("6.7.1", sha256="d6950597ce1fc2e1cf374c3aa70c2d72532bb74150e9853d7127af86a8a6c7b4")
    version("6.7.0", sha256="e17f016ec987092423e86d732c0f9786124598877fa00970fd806da113c02ca5")
    version("6.6.3", sha256="11abfcae323d295129f644f1828064e05af7d64d49edb0e00bfb8e8cb9691259")
    version("6.6.2", sha256="2cbdc4791c5838fddb1ce7ee693b165bb4acf3f81acd6c1bf9e56413b25050df")
    version("6.6.1", sha256="eb091c56e8c572d35d3da36f94f9e228892d43aecb559fa4728a19f0e44914c4")
    version("6.6.0", sha256="882f39ea3a40a0894cd64e515ce51711a4fab79b8c47bc0fe0279e99493a62cf")
    version("6.5.3", sha256="174021c4a630df2e7e912c2e523844ad3cb5f90967614628fd8aa15ddbab8bc5")
    version("6.5.2", sha256="221cafd400c0a992a42746b43ea879d23869232e56d9afe72cb191363267c674")
    version("6.5.1", sha256="fdde60cdc5c899ab7165f1c3f7b93bc727c2484c348f367d155604f5d901bfb6")
    version("6.5.0", sha256="7b0de20e177335927c55c58a3e1a7e269e32b044936e97e9a82564f0f3e69f99")
    version("6.4.3", sha256="e156692029a5503bad5f681bda856dd9df9dec17baa0ca7ee36b10178503ed40")
    version("6.4.2", sha256="c138ae734cfcde7a92a7efd97a902e53f3cd2c2f89606dfc482d0756f60cdc23")
    version("6.4.1", sha256="0ef6db6b3e1074e03dcae7e689144af66fd51b95a6efe949d40281cc43e6fecf")
    version("6.4.0", sha256="fbc462816bf5b87d521e9f69cebe0ce331de2258396e0932fa580283f07fce0c")
    version("6.3.2", sha256="95b78830a99f417ff34ee784ab78f5eeb7bb12adb16d137c3026434c44a904dd")
    version("6.3.1", sha256="4393e8cea0c58b1e0e901735fcffad141261576a0fa414ed6309910ac3d49df9")
    version("6.3.0", sha256="c50dc73f633e6c0f6ee3f51980c698800f1a0cadb423679bcef18e446ac72138")
    version("6.2.4", sha256="657d1405b5e15afcf322cc75b881f62d6a56f16383707742a99eb87f53cb63de")
    version("6.2.3", sha256="2dd095fa82bff9e0feb7a9004c1b2fb910f79ecc6111aa64637c95a02b7a8abb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("dbus", default=False, description="Build with D-Bus support.")
    variant(
        "framework", default=bool(MACOS_VERSION), description="Build as a macOS Framework package."
    )
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("network", default=False, description="Build with SSL support.")

    # GUI-only dependencies
    variant(
        "accessibility",
        default=False,
        when="+gui",
        description="Build with accessibility support.",
    )
    variant("gtk", default=False, when="+gui", description="Build with gtkplus.")
    variant("opengl", default=False, when="+gui", description="Build with OpenGL support.")
    variant("widgets", default=True, when="+gui", description="Build with widgets.")

    # Dependencies, then variant- and version-specific dependencies
    depends_on("cmake@3.21:", type="build", when="~shared")
    depends_on("cmake@3.21:", type="build", when="platform=darwin")
    depends_on("double-conversion")
    depends_on("icu4c")
    depends_on("libxml2")
    depends_on("pcre2+multibyte")
    depends_on("zlib-api")
    depends_on("zstd")
    with when("platform=linux"):
        depends_on("libdrm")
        depends_on("at-spi2-core", when="+accessibility")
    depends_on("dbus", when="+dbus")
    depends_on("gl", when="+opengl")
    depends_on("sqlite", when="+sql")

    with when("+gui"):
        depends_on("fontconfig")
        depends_on("freetype")
        depends_on("harfbuzz")
        depends_on("jpeg")
        depends_on("libpng")
        with when("platform=linux"):
            depends_on("libxkbcommon")
            depends_on("libxcb@1.13:")  # requires xinput
            depends_on("libxrender")
            depends_on("libx11")
            depends_on("xcb-util")
            depends_on("xcb-util-cursor")
            depends_on("xcb-util-image")
            depends_on("xcb-util-keysyms")
            depends_on("xcb-util-renderutil")
            depends_on("xcb-util-wm")

    with when("+network"):
        depends_on("openssl")
        with when("platform=linux"):
            depends_on("libproxy")

    # Qt6 requires newer compilers: see https://github.com/spack/spack/issues/34418
    conflicts("%gcc@:7")
    # The oldest compiler for Qt 6.5 is GCC 9: https://doc.qt.io/qt-6.5/supported-platforms.html
    with when("@6.5:"):
        conflicts("%gcc@:8")

    # ensure that Qt links against GSS framework on macOS: https://bugreports.qt.io/browse/QTBUG-114537
    with when("@6.3.2:6.5.1"):
        patch(
            "https://github.com/qt/qtbase/commit/c3d3e7312499189dde2ff9c0cb14bd608d6fd1cd.patch?full_index=1",
            sha256="85c16db15406b0094831bb57016dab7e0c0fd0978b082a1dc103c87334db7915",
        )
    with when("@6.3.2:6.5.2"):
        patch(
            "https://github.com/qt/qtbase/commit/1bf144ba78ff10d712b4de55d2797b9256948a1d.patch?full_index=1",
            sha256="e4d9f1aee0566558e77eef5609b63c1fde3f3986bea1b9d5d7930b297f916a5e",
        )

    @property
    def archive_files(self):
        """Save both the CMakeCache and the config summary."""
        return [
            join_path(self.build_directory, filename)
            for filename in ["CMakeCache.txt", "config.summary"]
        ]

    vendor_deps_to_remove = [
        "double-conversion",
        "freetype",
        "harfbuzz-ng",
        "libjpeg",
        "libpng",
        "libpsl",
    ]

    def cmake_args(self):
        spec = self.spec

        args = super().cmake_args()

        def define(cmake_var, value):
            args.append(self.define(cmake_var, value))

        def define_from_variant(cmake_var, variant=None):
            result = self.define_from_variant(cmake_var, variant)
            if result:
                # Not a conditional variant
                args.append(result)

        def define_feature(key, variant=None):
            if variant is None:
                variant = key
            define_from_variant("FEATURE_" + key, variant)

        define_from_variant("BUILD_SHARED_LIBS", "shared")
        define("FEATURE_optimize_size", spec.satisfies("build_type=MinSizeRel"))

        # Top-level features
        define_feature("accessibility")
        # concurrent: default to on
        define_feature("dbus")
        define_feature("framework")
        define_feature("gui")
        define_feature("network")  # note: private feature
        # testlib: default to on
        # thread: default to on
        define_feature("widgets")  # note: private feature
        define_feature("sql")  # note: private feature
        # xml: default to on

        # Extra FEATURE_ toggles
        features = []
        if "+dbus" in spec:
            features.append("dbus_linked")
        if "+network" in spec:
            features.extend(["openssl_linked", "openssl"])
            if sys.platform == "linux":
                features.append("libproxy")
        for k in features:
            define("FEATURE_" + k, True)

        if "~opengl" in spec:
            args.append(self.define("INPUT_opengl", "no"))

        # INPUT_* arguments: undefined/no/qt/system
        sys_inputs = ["doubleconversion"]
        if "+sql" in spec:
            sys_inputs.append("sqlite")
        for k in sys_inputs:
            define("INPUT_" + k, "system")

        # FEATURE_system_* arguments: on/off
        sys_features = [
            ("doubleconversion", True),
            ("pcre2", True),
            ("zlib", True),
            ("libb2", False),
        ]
        if "+gui" in spec:
            sys_features += [
                ("jpeg", True),
                ("png", True),
                ("sqlite", True),
                ("freetype", True),
                ("harfbuzz", True),
                ("textmarkdownreader", False),
            ]
            with when("platform=linux"):
                sys_features += [("xcb_xinput", True)]
        if "+network" in spec:
            sys_features += [("proxies", True)]
        for k, v in sys_features:
            define("FEATURE_system_" + k, v)

        return args

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(self.spec.prefix.bin.qmake)
