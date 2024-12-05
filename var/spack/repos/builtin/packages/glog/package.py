# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glog(CMakePackage):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url = "https://github.com/google/glog/archive/v0.3.5.tar.gz"

    license("BSD-3-Clause")

    version("0.7.1", sha256="00e4a87e87b7e7612f519a41e491f16623b12423620006f59f5688bfd8d13b08")
    version("0.7.0", sha256="375106b5976231b92e66879c1a92ce062923b9ae573c42b56ba28b112ee4cc11")
    version("0.6.0", sha256="8a83bf982f37bb70825df71a9709fa90ea9f4447fb3c099e1d720a439d88bad6")
    version("0.4.0", sha256="f28359aeba12f30d73d9e4711ef356dc842886968112162bc73002645139c39c")
    version("0.3.5", sha256="7580e408a2c0b5a89ca214739978ce6ff480b5e7d8d7698a2aa92fadc484d1e0")

    depends_on("cxx", type="build")  # generated

    depends_on("gflags")

    depends_on("cmake@3:", type="build")
    depends_on("cmake@3.16:", type="build", when="@0.6.0:")
    depends_on("cmake@3.22:", type="build", when="@0.7.0:")

    def cmake_args(self):
        return [self.define("BUILD_SHARED_LIBS", True)]
