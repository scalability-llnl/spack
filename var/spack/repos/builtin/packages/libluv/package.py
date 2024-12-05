# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libluv(CMakePackage):
    """This library makes libuv available to lua scripts.
    It was made for the luvit project but should usable from nearly
    any lua project."""

    homepage = "https://github.com/luvit/luv"
    url = "https://github.com/luvit/luv/releases/download/1.36.0-0/luv-1.36.0-0.tar.gz"

    license("Apache-2.0")

    version("1.48.0-2", sha256="2c3a1ddfebb4f6550293a40ee789f7122e97647eede51511f57203de48c03b7a")
    version("1.45.0-0", sha256="fa6c46fb09f88320afa7f88017efd7b0d2b3a0158c5ba5b6851340b0332a2b81")
    version("1.44.2-1", sha256="3eb5c7bc44f61fbc4148ea30e3221d410263e0ffa285672851fc19debf9e5c30")
    version("1.44.2-0", sha256="30639f8e0fac7fb0c3a04b94a00f73c6d218c15765347ceb0998a6b72464b6cf")
    version("1.43.0-0", sha256="567a6f3dcdcf8a9b54ddc57ffef89d1e950d72832b85ee81c8c83a9d4e0e9de2")
    version("1.42.0-1", sha256="4b6fbaa89d2420edf6070ad9e522993e132bd7eb2540ff754c2b9f1497744db2")
    version("1.42.0-0", sha256="b5228a9d0eaacd9f862b6270c732d5c90773a28ce53b6d9e32a14050e7947f36")
    version("1.36.0-0", sha256="f2e7eb372574f25c6978c1dc74280d22efdcd7df2dda4a286c7fe7dceda26445")

    depends_on("c", type="build")  # generated

    # https://github.com/neovim/neovim/issues/25770
    # up to 1.45 (included) dynamic library on macOS did not have the @rpath prefix, being not
    # usable on this platform.
    # from 1.46, by requiring a newer cmake version, CMP0042 is in place and it works correctly.
    depends_on("cmake@3:", type="build")

    depends_on("lua-lang", type="link")
    depends_on("libuv", type="link")

    def cmake_args(self):
        args = [
            self.define("CMAKE_POLICY_DEFAULT_CMP0042", "NEW"),
            "-DLUA_BUILD_TYPE=System",
            "-DBUILD_STATIC_LIBS=ON",
            "-DBUILD_SHARED_LIBS=ON",
            "-DWITH_SHARED_LIBUV=ON",
        ]
        return args
