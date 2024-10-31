# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LuaSol2(CMakePackage):
    """sol2 is a C++ library binding to Lua."""

    homepage = "https://sol2.rtfd.io"
    url = "https://github.com/ThePhD/sol2/archive/refs/tags/v3.2.2.tar.gz"
    git = "https://github.com/ThePhD/sol2.git"

    maintainers("rbberger")

    license("MIT")

    version("develop", branch="develop")
    version("3.3.0", tag="v3.3.0", commit="eba86625b707e3c8c99bbfc4624e51f42dc9e561")
    version("3.2.3", sha256="f74158f92996f476786be9c9e83f8275129bb1da2a8d517d050421ac160a4b9e")
    version("3.2.2", sha256="141790dae0c1821dd2dbac3595433de49ba72545845efc3ec7d88de8b0a3b2da")
    version("3.2.1", sha256="b10f88dc1246f74a10348faef7d2c06e2784693307df74dcd87c4641cf6a6828")
    version("3.2.0", sha256="733f03d82df6e0e8a15967831840d240dcb2c606982bec753bd173a9cc1b3435")
    version("3.0.3", sha256="bf089e50387edfc70063e24fd7fbb693cceba4a50147d864fabedd1b33483582")
    version("3.0.2", sha256="3f5f369eae6732ae9a315fe4370bbdc9900d2f2f4f291206aeb5b2d5533f0c99")

    depends_on("cxx", type="build")  # generated

    # Lua is not needed when building, since sol2 is headers-only
    depends_on("lua", type=("link", "run"))

    def cmake_args(self):
        args = [
            self.define("SOL2_ENABLE_INSTALL", True),
            self.define("SOL2_BUILD_LUA", False),
            self.define("SOL2_LUA_VERSION", self.spec["lua"].version),
        ]
        return args
