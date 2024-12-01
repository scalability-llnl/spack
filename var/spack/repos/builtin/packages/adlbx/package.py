# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Adlbx(AutotoolsPackage):
    """ADLB/X: Master-worker library + work stealing and data dependencies"""

    homepage = "http://swift-lang.org/Swift-T"
    url = "https://swift-lang.github.io/swift-t-downloads/spack/adlbx-1.0.0.tar.gz"
    git = "https://github.com/swift-lang/swift-t.git"

    version("master", branch="master")
    version("1.0.0", sha256="9d547b1d36e5af1b11c97d0b700c6cb1fec2661cf583553e22b090e3619caba7")
    version("0.9.2", sha256="524902d648001b689a98492402d754a607b8c1d0734699154063c1a4f3410d4a")
    version("0.9.1", sha256="8913493fe0c097ff13c721ab057514e5bdb55f6318d4e3512692ab739c3190b3")

    depends_on("c", type="build")  # generated

    depends_on("exmcutils@master", when="@master")
    depends_on("exmcutils@:0.5.7", when="@:0.9.2")
    depends_on("exmcutils", when="@0.9.1:")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("m4", type="build", when="@master")
    depends_on("mpi")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CC", spec["mpi"].mpicc)
        env.set("CXX", spec["mpi"].mpicxx)
        env.set("CXXLD", spec["mpi"].mpicxx)

    @property
    def configure_directory(self):
        if self.version == Version("master"):
            return "lb/code"
        else:
            return "."

    def configure_args(self):
        args = ["--with-c-utils=" + self.spec["exmcutils"].prefix]
        return args
