# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TclTogl(AutotoolsPackage):
    """Tcl-Togl provides a platform independent Tcl/Tk widget for using OpenGL rendering contexts"""

    homepage = "https://togl.sourceforge.net/"
    url = "https://kumisystems.dl.sourceforge.net/project/togl/Togl/2.0/Togl2.0-src.tar.gz"

    version("2.0", sha256="b7d4a90bbad3aca618d505ee99e7fd8fb04c829f63231dda2360f557ba3f7610")

    variant("64bit", default=False, description="Build and link with shared libraries")
    variant("64bit-vis", default=False, description="Enable 64bit Sparc VIS support")
    variant("load", default=True, description='Allow dynamic loading and "load" command')
    variant("rpath", default=False, description="Disable rpath support")
    variant("shared", default=True, description="Build and link with shared libraries")
    variant("stubs", default=True, description="Build and link with stub libraries")
    variant("symbols", default=True, description="Build with debugging symbols")
    variant("threads", default=True, description="Build with threads")
    variant("wince", default=False, description="Enable Win/CE support")

    depends_on("autoconf", type="build", when="build_system=autotools")
    depends_on("automake", type="build", when="build_system=autotools")
    depends_on("libtool", type="build", when="build_system=autotools")
    depends_on("mesa~llvm")

    depends_on("tk@8.1:")
    depends_on("tcl@8.1:")

    extends("tcl")

    def configure_args(self):
        args = []

        for enable_variant in (
            "64bit",
            "64bit-vis",
            "load",
            "rpath",
            "shared",
            "stubs",
            "symbols",
            "threads",
            "wince",
        ):
            args.extend(self.enable_or_disable(enable_variant))

        for with_dep in ("tcl", "tk"):
            args.append("--with-" + with_dep + "={0}".format(self.spec[with_dep].prefix.lib))

        return args

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path(
            "LD_LIBRARY_PATH",
            join_path(self.spec["tcl"].prefix.lib, "Togl" + str(self.version.up_to(2))),
        )
