# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MsgpackC(CMakePackage):
    """A small, fast binary interchange format convertible to/from JSON"""

    homepage = "http://www.msgpack.org"
    url = "https://github.com/msgpack/msgpack-c/archive/cpp-3.0.1.tar.gz"

    license("BSL-1.0")

    version("3.1.1", sha256="bda49f996a73d2c6080ff0523e7b535917cd28c8a79c3a5da54fc29332d61d1e")
    version("3.0.1", sha256="1b834ab0b5b41da1dbfb96dd4a673f6de7e79dbd7f212f45a553ff9cc54abf3b")
    version(
        "1.4.1",
        sha256="74324d696f9abb75d8a7cd5e77add5062592b7eac386c8102de78a6cc5309886",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost", when="@4:")
    depends_on("cmake@2.8.0:", type="build")
    depends_on("cmake@3.1.0:", type="build", when="@4:")
    depends_on("googletest", type="test")

    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_FLAGS", "-Wno-implicit-fallthrough"),
            self.define("CMAKE_C_FLAGS", "-Wno-implicit-fallthrough"),
            self.define("MSGPACK_BUILD_TESTS", self.run_tests),
        ]
        return args
