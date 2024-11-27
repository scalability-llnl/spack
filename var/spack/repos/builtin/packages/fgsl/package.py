# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

#
# Author: Gilbert Brietzke
# Date: June 18, 2019


class Fgsl(AutotoolsPackage):
    """Fortran interface to the GNU Scientific Library"""

    homepage = "https://github.com/reinh-bader/fgsl"
    url = "https://github.com/reinh-bader/fgsl/archive/v1.2.0.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.5.0",
        sha256="5013b4e000e556daac8b3c83192adfe8f36ffdc91d1d4baf0b1cb3100260e664",
        url="https://github.com/reinh-bader/fgsl/archive/1.5.0.tar.gz",
    )
    version("1.4.0", sha256="9d1d0353013ffa5e95389b1ebeaa68f258c949bdae2feb3f4d3afce7bd274c87")
    version("1.3.0", sha256="6d73d558c889d7ea23e510a436f28618624035e8ffa07692894f10968aa83a4b")
    version("1.2.0", sha256="e5a4ac08eb744c963e95a46a51d76c56593836077c5ad8c47e240cae57027002")
    version("1.1.0", sha256="a5adce3c3b279d2dacc05b74c598ff89be7ef3ae3ec59b3ec1355750c1bb4832")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gsl@2.6", when="@1.5.0")
    depends_on("gsl@2.5", when="@1.4.0")
    depends_on("gsl@2.4", when="@1.3.0")
    depends_on("gsl@2.3", when="@1.2.0")
    depends_on("gsl@2.2.1", when="@1.1.0")

    parallel = False

    @run_before("autoreconf")
    def create_m4_dir(self):
        mkdir("m4")

    def setup_build_environment(self, env):
        if self.compiler.name == "gcc":
            env.append_flags("FCFLAGS", "-ffree-line-length-none")
