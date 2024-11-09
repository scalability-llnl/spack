# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.hooks.sbang as sbang
from spack.package import *


class GobjectIntrospection(MesonPackage, AutotoolsPackage):
    """The GObject Introspection is used to describe the program APIs and
    collect them in a uniform, machine readable format.Cairo is a 2D graphics
    library with support for multiple output
    """

    homepage = "https://wiki.gnome.org/Projects/GObjectIntrospection"
    url = "https://download.gnome.org/sources/gobject-introspection/1.72/gobject-introspection-1.72.0.tar.xz"

    maintainers("michaelkuhn")

    license("LGPL-2.0-or-later AND GPL-2.0-or-later AND MIT")

    version("1.78.1", sha256="bd7babd99af7258e76819e45ba4a6bc399608fe762d83fde3cac033c50841bb4")
    version("1.76.1", sha256="196178bf64345501dcdc4d8469b36aa6fe80489354efe71cb7cb8ab82a3738bf")
    version("1.72.1", sha256="012e313186e3186cf0fde6decb57d970adf90e6b1fac5612fe69cbb5ba99543a")
    version("1.72.0", sha256="02fe8e590861d88f83060dd39cda5ccaa60b2da1d21d0f95499301b186beaabc")
    version("1.60.2", sha256="ffdfe2368fb2e34a547898b01aac0520d52d8627fdeb1c306559bcb503ab5e9c")
    version("1.56.1", sha256="5b2875ccff99ff7baab63a34b67f8c920def240e178ff50add809e267d9ea24b")
    version("1.49.2", sha256="73d59470ba1a546b293f54d023fd09cca03a951005745d86d586b9e3a8dde9ac")
    version("1.48.0", sha256="fa275aaccdbfc91ec0bc9a6fd0562051acdba731e7d584b64a277fec60e75877")

    depends_on("c", type="build")  # generated

    build_system(
        conditional("autotools", when="@:1.60"),
        conditional("meson", when="@1.61:"),
        default="meson",
    )

    depends_on("pkgconfig", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")

    # Does not build with sed from Darwin
    depends_on("sed", when="platform=darwin", type="build")

    depends_on("cairo+gobject")
    depends_on("glib@2.78:", when="@1.78")
    depends_on("glib@2.76:", when="@1.76")
    depends_on("glib@2.58:", when="@1.60:1.72")
    depends_on("glib@2.56:", when="@1.56")
    depends_on("glib@2.49.2:", when="@1.49.2")
    depends_on("glib@2.48.1", when="@1.48.0")

    depends_on("libffi")
    # https://gitlab.gnome.org/GNOME/gobject-introspection/-/merge_requests/283
    depends_on("libffi@:3.3", when="@:1.72")  # libffi 3.4 caused seg faults
    depends_on("python")

    # This package creates several scripts from
    # toosl/g-ir-tool-template.in.  In their original form these
    # scripts end up with a sbang line like
    #
    # `#!/usr/bin/env /path/to/spack/python`.
    #
    # These scripts are generated and then used as part of the build
    # (other packages also use the scripts after they've been
    # installed).
    #
    # The path to the spack python can become too long.  Because these
    # tools are used as part of the build, the normal hook that fixes
    # this problem can't help us.
    # This package fixes the problem in two steps:
    # - it rewrites the g-ir-tool-template so that its sbang line
    #   refers directly to spack's python (filter_file step below); and
    # - it patches the Makefile.in so that the generated Makefile has an
    #   extra sed expression in its TOOL_SUBSTITUTION that results in
    #   an `#!/bin/bash /path/to/spack/bin/sbang` unconditionally being
    #   inserted into the scripts as they're generated.
    patch("sbang.patch", when="@:1.56")
    # The TOOL_SUBSITUTION line changed after 1.58 to include /usr/bin/env in
    # the Python substituion more explicitly. The Makefile.am was removed in 1.61.
    patch("sbang-1.60.2.patch", when="@1.58:1.60")

    # Drop deprecated xml.etree.ElementTree.Element.getchildren() which leads
    # to compilation issues with Python 3.9.
    # https://gitlab.gnome.org/GNOME/gobject-introspection/-/issues/325
    patch(
        "https://gitlab.gnome.org/GNOME/gobject-introspection/-/commit/"
        "1f9284228092b2a7200e8a78bc0ea6702231c6db.diff",
        sha256="dcb9e7c956dff49c3a73535829382e8662fa6bd13bdfb416e8eac47b2604fa0a",
        when="@:1.63.1",
    )

    conflicts(
        "^python@3.11:",
        when="@:1.60",
        msg="giscannermodule.c in <=v1.60 uses syntax incompatible with Python >=3.11",
    )

    def url_for_version(self, version):
        url = "https://download.gnome.org/sources/gobject-introspection/{0}/gobject-introspection-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        # Only needed for sbang.patch above
        if self.spec.satisfies("@:1.60"):
            env.set("SPACK_SBANG", sbang.sbang_install_path())

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    @property
    def parallel(self):
        return not self.spec.satisfies("%fj")


class AutotoolsBuilderPackage(spack.build_systems.autotools.AutotoolsBuilder):
    @run_before("build")
    def filter_file_to_avoid_overly_long_shebangs(self):
        # we need to filter this file to avoid an overly long hashbang line
        filter_file("#!/usr/bin/env @PYTHON@", "#!@PYTHON@", "tools/g-ir-tool-template.in")
