# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsimd(CMakePackage):
    """C++ wrappers for SIMD intrinsics"""

    homepage = "https://quantstack.net/xsimd"
    url = "https://github.com/QuantStack/xsimd/archive/3.1.0.tar.gz"
    git = "https://github.com/QuantStack/xsimd.git"

    maintainers("ax3l")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("8.1.0", sha256="d52551360d37709675237d2a0418e28f70995b5b7cdad7c674626bcfbbf48328")
    version("8.0.5", sha256="0e1b5d973b63009f06a3885931a37452580dbc8d7ca8ad40d4b8c80d2a0f84d7")
    version("8.0.4", sha256="5197529e7ca715ddfcae7c5c4097879c86dae6ef85f3f67c402e2e6c5e803c41")
    version("8.0.3", sha256="d1d41253c4f82eaf2f369d7fcb4142e35076cf8675b9d94caa06ecf883024344")
    version("8.0.2", sha256="91ef266f28ab4e62cb43f28630b6519ac9fbce3aeab5e538de8bd02401a616f3")
    version("8.0.1", sha256="21b4700e9ef70f6c9a86952047efd8272317df4e6fee35963de9394fd9c5677f")
    version("8.0.0", sha256="6b0e74f419cde47b61a314db167ebefe38c4d066db5ae7ac4341f717485f7228")
    version("7.6.0", sha256="eaf47f1a316ef6c3287b266161eeafc5aa61226ce5ac6c13502546435b790252")
    version("7.5.0", sha256="45337317c7f238fe0d64bb5d5418d264a427efc53400ddf8e6a964b6bcb31ce9")
    version("7.4.10", sha256="df00f476dea0c52ffebad60924e3f0db2a016b80d508f8d5a2399a74c0d134cd")
    version("7.4.9", sha256="f6601ffb002864ec0dc6013efd9f7a72d756418857c2d893be0644a2f041874e")
    version("7.2.3", sha256="bbc673ad3e9d4523503a4222da05886e086b0e0bd6bd93d03ea3b663c74297b9")
    version("4.0.0", sha256="67b818601c15ef15ea4d611a8cd7382588c340ebd9146c799a0210d212540455")
    version("3.1.0", sha256="d56288826f6b82fd9583f83ace6aa2306ba2ae82cec003de1d04ce17fbb1e91f")

    depends_on("cxx", type="build")  # generated

    depends_on("googletest", type="test")

    # C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.6")
    # untested: conflicts('%intel@:15')
    # untested: conflicts('%pgi@:14')

    def cmake_args(self):
        args = [self.define("BUILD_TESTS", self.run_tests)]

        return args
