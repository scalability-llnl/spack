# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yorick(Package):
    """Yorick is an interpreted programming language for scientific simulations
    or calculations, postprocessing or steering large simulation codes,
    interactive scientific graphics, and reading, writing, or translating
    files of numbers. Yorick includes an interactive graphics package, and a
    binary file package capable of translating to and from the raw numeric
    formats of all modern computers. Yorick is written in ANSI C and runs on
    most operating systems (*nix systems, MacOS X, Windows).
    """

    homepage = "https://dhmunro.github.io/yorick-doc/"
    url = "https://github.com/dhmunro/yorick/archive/y_2_2_04.tar.gz"
    git = "https://github.com/dhmunro/yorick.git"

    version("master", branch="master")
    version("2.2.04", sha256="4a4f3a18aed533cc5fadbb3d4bafb48f04834a22cbff6ad5c19d9dba74facbda")
    version("f90-plugin", branch="f90-plugin")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("X", default=False, description="Enable X11 support")

    depends_on("libx11", when="+X")

    extendable = True

    def url_for_version(self, version):
        url = "https://github.com/dhmunro/yorick/archive/y_{0}.tar.gz"
        return url.format(version.underscored)

    def setup_build_environment(self, env):
        env.set("FORTRAN_LINKAGE", "-Df_linkage")
        if self.spec.satisfies("arch=aarch64:"):
            env.set("FPU_IGNORE", "1")

    def install(self, spec, prefix):
        make("config")

        filter_file(r"^CC.+", "CC={0}".format(self.compiler.cc), "Make.cfg")
        filter_file(r"^FC.+", "FC={0}".format(self.compiler.fc), "Make.cfg")
        filter_file(r"^COPT_DEFAULT.+", "COPT_DEFAULT=-O3", "Make.cfg")

        make()
        make("install")

        install_tree("relocate", prefix)
