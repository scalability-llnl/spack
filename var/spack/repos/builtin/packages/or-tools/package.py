# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class OrTools(CMakePackage):
    """This project hosts operations research tools developed at
    Google and made available as open source under the Apache 2.0
    License."""

    homepage = "https://developers.google.com/optimization/"
    url = "https://github.com/google/or-tools/archive/v7.8.tar.gz"
    maintainers("hyoklee")

    license("Apache-2.0")

    version("7.8", sha256="d93a9502b18af51902abd130ff5f23768fcf47e266e6d1f34b3586387aa2de68")

    depends_on("cxx", type="build")  # generated
    variant("coin", default=False, description="Enable COIN-OR solvers.")
    depends_on("cmake@3.14:", type="build")
    depends_on("gflags@2.2.2:")
    depends_on("glog@0.4.0:")
    depends_on("protobuf@3.12.2:")
    depends_on("abseil-cpp@20200225.2:")
    depends_on("cbc@2.10.5:")
    depends_on("cgl@0.60.3:")
    depends_on("clp@1.17.4:")
    depends_on("osi@0.108.6:")
    depends_on("coinutils@2.11.4:", when="+coin")

    def cmake_args(self):
        cmake_args = []
        cmake_args.append("-DBUILD_DEPS=OFF")
        cmake_args.append("-DBUILD_PYTHON=OFF")
        cmake_args.append(self.define_from_variant("USE_COINOR", "coin"))
        cmake_args.append("-DUSE_SCIP=ON")
        cmake_args.append("-DBUILD_SCIP=ON")
        cmake_args.append("-DBUILD_TESTING=OFF")
        return cmake_args
