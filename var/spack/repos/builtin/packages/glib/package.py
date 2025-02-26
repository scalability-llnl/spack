# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.build_systems.meson
from spack.package import *
from spack.util.environment import is_system_path


class Glib(MesonPackage):
    """GLib provides the core application building blocks for libraries and applications written
    in C.

    The GLib package contains a low-level libraries useful for providing data structure handling
    for C, portability wrappers and interfaces for such runtime functionality as an event loop,
    threads, dynamic loading and an object system.
    """

    homepage = "https://developer.gnome.org/glib/"
    url = "https://download.gnome.org/sources/glib/2.82/glib-2.82.2.tar.xz"
    list_url = "https://download.gnome.org/sources/glib"
    list_depth = 1

    maintainers("michaelkuhn")

    license("LGPL-2.1-or-later")

    # Even minor versions are stable, odd minor versions are development, only add even numbers
    version("2.82.2", sha256="ab45f5a323048b1659ee0fbda5cecd94b099ab3e4b9abf26ae06aeb3e781fd63")
    version("2.78.3", sha256="609801dd373796e515972bf95fc0b2daa44545481ee2f465c4f204d224b2bc21")
    version("2.78.0", sha256="44eaab8b720877ce303c5540b657b126f12dc94972d9880b52959f43fb537b30")
    version("2.76.6", sha256="1136ae6987dcbb64e0be3197a80190520f7acab81e2bfb937dc85c11c8aa9f04")
    version("2.76.4", sha256="5a5a191c96836e166a7771f7ea6ca2b0069c603c7da3cba1cd38d1694a395dda")
    version("2.76.3", sha256="c0be444e403d7c3184d1f394f89f0b644710b5e9331b54fa4e8b5037813ad32a")
    version("2.76.2", sha256="24f3847857b1d8674cdb0389a36edec0f13c666cd3ce727ecd340eb9da8aca9e")
    version("2.76.1", sha256="43dc0f6a126958f5b454136c4398eab420249c16171a769784486e25f2fda19f")
    version("2.74.7", sha256="196ab86c27127a61b7a70c3ba6af7b97bdc01c07cd3b21abd5e778b955eccb1b")
    version("2.74.6", sha256="069cf7e51cd261eb163aaf06c8d1754c6835f31252180aff5814e5afc7757fbc")
    version("2.74.3", sha256="e9bc41ecd9690d9bc6a970cc7380119b828e5b6a4b16c393c638b3dc2b87cbcb")
    version("2.74.1", sha256="0ab981618d1db47845e56417b0d7c123f81a3427b2b9c93f5a46ff5bbb964964")
    version("2.74.0", sha256="3652c7f072d7b031a6b5edd623f77ebc5dcd2ae698598abcc89ff39ca75add30")
    version("2.72.4", sha256="8848aba518ba2f4217d144307a1d6cb9afcc92b54e5c13ac1f8c4d4608e96f0e")
    version("2.72.3", sha256="4a39a2f624b8512d500d5840173eda7fa85f51c109052eae806acece85d345f0")
    version("2.72.2", sha256="78d599a133dba7fe2036dfa8db8fb6131ab9642783fc9578b07a20995252d2de")
    version("2.72.1", sha256="c07e57147b254cef92ce80a0378dc0c02a4358e7de4702e9f403069781095fe2")
    version("2.70.5", sha256="f70bf76ebcc84e0705722f038be8e2f9a58d17e1a700810c635fcc18b8974b7e")
    version("2.70.4", sha256="ab3d176f3115dcc4e5d02db795984e04e4f4b48d836252e23e8c468e9d423c33")
    version("2.70.2", sha256="0551459c85cd3da3d58ddc9016fd28be5af503f5e1615a71ba5b512ac945806f")
    version("2.70.0", sha256="200d7df811c5ba634afbf109f14bb40ba7fde670e89389885da14e27c0840742")
    version("2.68.4", sha256="62fd061d08a75492617e625a73e2c05e259f831acbb8e1f8b9c81f23f7993a3b")
    version("2.68.3", sha256="e7e1a3c20c026109c45c9ec4a31d8dcebc22e86c69486993e565817d64be3138")
    version("2.68.2", sha256="ecc7798a9cc034eabdfd7f246e6dd461cdbf1175fcc2e9867cc7da7b7309e0fb")
    version("2.66.8", sha256="97bc87dd91365589af5cbbfea2574833aea7a1b71840fd365ecd2852c76b9c8b")
    version("2.66.7", sha256="09f158769f6f26b31074e15b1ac80ec39b13b53102dfae66cfe826fb2cc65502")
    version("2.66.6", sha256="80fff9c63d2725834328071c42003c311f77f91caf2285195c587c62f5638329")
    version("2.66.2", sha256="ec390bed4e8dd0f89e918f385e8d4cfd7470b1ef7c1ce93ec5c4fc6e3c6a17c4")
    version("2.64.6", sha256="c36ee07a70164c71f046016fe6aaacd6368333c42590bc0cba47c344ffb853f1")
    version("2.64.5", sha256="9cbd5bd2715ead1c28d53c46f7b7b6ff6166f5887b772c1a9e3bf2910cfecc11")
    version("2.64.4", sha256="f7e0b325b272281f0462e0f7fff25a833820cac19911ff677251daf6d87bce50")
    version("2.64.3", sha256="fe9cbc97925d14c804935f067a3ad77ef55c0bbe9befe68962318f5a767ceb22")
    version("2.64.2", sha256="9a2f21ed8f13b9303399de13a0252b7cbcede593d26971378ec6cb90e87f2277")
    version("2.64.1", sha256="17967603bcb44b6dbaac47988d80c29a3d28519210b28157c2bd10997595bbc7")
    version("2.62.6", sha256="104fa26fbefae8024ff898330c671ec23ad075c1c0bce45c325c6d5657d58b9c")
    version("2.60.7", sha256="8b12c0af569afd3b71200556ad751bad4cf4bf7bc4b5f880638459a42ca86310")
    version("2.58.3", sha256="8f43c31767e88a25da72b52a40f3301fefc49a665b56dc10ee7cc9565cbe7481")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("libmount", default=False, description="Build with libmount support")
    variant(
        "tracing",
        values=any_combination_of("dtrace", "systemtap"),
        description="Enable tracing support",
    )

    with default_args(type="build"):
        depends_on("meson@1.4:", when="@2.83:")
        depends_on("meson@1.2:", when="@2.79:")
        depends_on("meson@0.60.0:", when="@2.73:")
        depends_on("meson@0.52.0:", when="@2.71:")
        depends_on("meson@0.49.2:", when="@2.61.2:")
        depends_on("meson@0.48.0:")
        depends_on("pkgconfig", type="build")

    depends_on("libffi")
    depends_on("zlib-api")
    depends_on("gettext")
    depends_on("perl", type=("build", "run"))
    extends("python", type=("build", "run"))
    # Uses distutils in gio/gdbus-2.0/codegen/utils.py
    depends_on("python@:3.11", type=("build", "run"), when="@:2.78")
    depends_on("pcre2", when="@2.73.2:")
    depends_on("pcre2@10.34:", when="@2.74:")
    depends_on("pcre+utf", when="@:2.73.1")
    depends_on("uuid", when="+libmount")
    depends_on("util-linux", when="+libmount")
    depends_on("iconv")
    depends_on("elf")  # bin/gresource

    # glib prefers the libc version of gettext, which breaks the build if the
    # external version is also found.
    patch("meson-gettext.patch", when="@:2.64")
    patch("meson-gettext-2.66.patch", when="@2.66:2.68,2.72")
    patch("meson-gettext-2.70.patch", when="@2.70")

    def url_for_version(self, version):
        return f"https://download.gnome.org/sources/glib/{version.up_to(2)}/glib-{version}.tar.xz"

    def patch(self):
        """A few glib tests have external dependencies / try to access the X server"""
        # Surgically disable tests which we cannot make pass in a spack build
        gio_tests = FileFilter("gio/tests/meson.build")
        gio_tests.filter("if not glib_have_cocoa", "if false")
        gio_tests.filter("'contenttype' : {},", "")
        gio_tests.filter("'file' : {},", "")
        gio_tests.filter("'gdbus-peer'", "'file'")
        gio_tests.filter("'gdbus-address-get-session' : {},", "")
        filter_file("'mkenums.py'( : {})*,*", "", "gobject/tests/meson.build")
        filter_file("'fileutils' : {},", "", "glib/tests/meson.build")

    @property
    def libs(self):
        return find_libraries(["libglib*"], root=self.prefix, recursive=True)


class MesonBuilder(spack.build_systems.meson.MesonBuilder):

    @property
    def dtrace_copy_path(self):
        return join_path(self.stage.source_path, "dtrace-copy")

    @run_before("install", when="@:2.80")  # @2.81: uses meson found python abs path.
    def fix_python_path_before_install(self):
        filter_file(
            "^#!/usr/bin/env @PYTHON@",
            f"#!/usr/bin/env {os.path.basename(self.spec['python'].command.path)}",
            "gobject/glib-genmarshal.in",
            "gobject/glib-mkenums.in",
        )

    @run_after("install", when="@:2.80")
    def fix_python_path_after_install(self):
        # Revert shebang, so Spack's sbang hook can fix it up (we have to do
        # this after install because otherwise the install target will try
        # to rebuild files as filter_file updates the timestamps)
        python_path = os.path.basename(self.spec["python"].command.path)
        filter_file(
            f"^#!/usr/bin/env {os.path.basename(python_path)}",
            f"#!{self.spec['python'].command.path}",
            join_path(self.prefix.bin, "glib-genmarshal"),
            join_path(self.prefix.bin, "glib-mkenums"),
        )

    @run_before("install")
    def fix_dtrace_usr_bin_path(self):
        if not self.spec.satisfies("tracing=dtrace"):
            return

        # dtrace may cause glib build to fail because it uses
        # '/usr/bin/python' in the shebang. To work around that
        # we copy the original script into a temporary folder, and
        # change the shebang to '/usr/bin/env python'
        dtrace = which("dtrace").path
        dtrace_copy = join_path(self.dtrace_copy_path, "dtrace")

        with working_dir(self.dtrace_copy_path, create=True):
            copy(dtrace, dtrace_copy)
            filter_file(
                "^#!/usr/bin/python",
                f"#!/usr/bin/env {os.path.basename(self.spec['python'].command.path)}",
                dtrace_copy,
            )

        # To have our own copy of dtrace in PATH, we need to
        # prepend to PATH the temporary folder where it resides
        env["PATH"] = ":".join([self.dtrace_copy_path] + env["PATH"].split(":"))

    @run_after("install")
    def gettext_libdir(self):
        # Packages that link to glib were also picking up -lintl from glib's
        # glib-2.0.pc file. However, packages such as py-pygobject were
        # bypassing spack's compiler wrapper for linking and thus not finding
        # the gettext library directory. The patch below explicitly adds the
        # appropriate -L path.
        spec = self.spec
        if (
            spec.satisfies("@2")
            and "intl" in spec["gettext"].libs.names
            and not is_system_path(spec["gettext"].prefix)
        ):
            filter_file(
                "Libs:",
                "Libs: -L{0} -Wl,-rpath={0} ".format(spec["gettext"].libs.directories[0]),
                join_path(self.spec["glib"].libs.directories[0], "pkgconfig", "glib-2.0.pc"),
            )

    def meson_args(self):
        args = []
        if self.spec.satisfies("@2.63.5:"):
            if self.spec.satisfies("+libmount"):
                args.append("-Dlibmount=enabled")
            else:
                args.append("-Dlibmount=disabled")
        else:
            if self.spec.satisfies("+libmount"):
                args.append("-Dlibmount=true")
            else:
                args.append("-Dlibmount=false")
        if self.spec.satisfies("tracing=dtrace"):
            args.append("-Ddtrace=true")
        else:
            args.append("-Ddtrace=false")
        if self.spec.satisfies("tracing=systemtap"):
            args.append("-Dsystemtap=true")
        else:
            args.append("-Dsystemtap=false")
        if self.spec.satisfies("@2.59.0:"):
            args.append("-Dselinux=disabled")
        else:
            args.append("-Dselinux=false")
        args.append("-Dgtk_doc=false")
        args.append("-Dlibelf=enabled")

        # arguments for older versions
        if self.spec.satisfies("@:2.72"):
            args.append("-Dgettext=external")
        if self.spec.satisfies("@:2.74"):
            if self.spec["iconv"].name == "libiconv":
                if self.spec.satisfies("@2.61.0:"):
                    args.append("-Diconv=external")
                else:
                    args.append("-Diconv=gnu")
            else:
                args.append("-Diconv=libc")
        return args
