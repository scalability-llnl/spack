# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openvkl(CMakePackage):
    """Intel® Open Volume Kernel Library is a collection of high-performance volume
    computation kernels, developed at Intel."""

    homepage = "https://www.openvkl.org/"
    url = "https://www.github.com/OpenVKL/openvkl/archive/v1.0.0.tar.gz"
    git = "https://www.github.com/OpenVKL/openvkl.git"

    license("Apache-2.0")

    version("2.0.1", sha256="0c7faa9582a93e93767afdb15a6c9c9ba154af7ee83a6b553705797be5f8af62")
    version("2.0.0", sha256="469c3fba254c4fcdd84f8a9763d2e1aaa496dc123b5a9d467cc0a561e284c4e6")
    version("1.3.2", sha256="7704736566bf17497a3e51c067bd575316895fda96eccc682dae4aac7fb07b28")
    version("1.3.1", sha256="c9cefb6c313f2b4c0331e9629931759a6bc204ec00deed6ec0becad1670a1933")
    version("1.3.0", sha256="c6d4d40e6d232839c278b53dee1e7bd3bd239c3ccac33f49b465fc65a0692be9")
    version("1.2.0", sha256="dc468c2f0a359aaa946e04a01c2a6634081f7b6ce31b3c212c74bf7b4b0c9ec2")
    version("1.1.0", sha256="d193c75a2c57acd764649215b244c432694a0169da374a9d769a81b02a9132e9")
    version("1.0.1", sha256="55a7c2b1dcf4641b523ae999e3c1cded305814067d6145cc8911e70a3e956ba6")
    version("1.0.0", sha256="81ccae679bfa2feefc4d4b1ce72bcd242ba34d2618fbb418a1c2a05d640d16b4")
    version("0.13.0", sha256="974608259e3a5d8e29d2dfe81c6b2b1830aadeb9bbdc87127f3a7c8631e9f1bd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("embree@4", when="@1.3.2:")
    depends_on("embree@3.13.0:3", when="@:1.3.1")
    depends_on("embree@3.13.1:", when="@1.0.0:")
    depends_on("ispc@1.15.0:", type=("build"))
    depends_on("ispc@1.16.0:", when="@1.0.0:", type=("build"))
    depends_on("ispc@1.18:", when="@1.3:", type=("build"))
    depends_on("rkcommon@1.6.1:")
    depends_on("rkcommon@1.7.0:", when="@1.0.0:")
    depends_on("rkcommon@1.8.0:", when="@1.1:")
    depends_on("rkcommon@:1.10.0", when="@:1.3.1")
    depends_on("rkcommon@1.11.0:", when="@1.3.2:")
    depends_on("rkcommon@:1.11.0", when="@:1.3.2")
    depends_on("tbb")

    def cmake_args(self):
        args = [
            # otherwise, openvkl 1.3.2 tries to install its headers into /openvkl
            self.define("CMAKE_INSTALL_INCLUDEDIR", f"{self.spec.prefix}/include"),
            self.define("BUILD_BENCHMARKS", False),
            self.define("BUILD_EXAMPLES", False),
            self.define("BUILD_TESTING", False),
        ]
        return args
