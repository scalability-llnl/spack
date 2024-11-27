# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JediCmake(CMakePackage):
    """CMake/ecbuild toolchains to facilitate portability on different systems."""

    homepage = "https://github.com/JCSDA/jedi-cmake"
    git = "https://github.com/JCSDA/jedi-cmake.git"

    maintainers("climbfuji")

    license("Apache-2.0")

    version("master", branch="master", no_cache=True)
    version("develop", branch="develop", no_cache=True)
    version(
        "1.4.0", commit="36fc99bdff5d3d8835480b37a3dcc75e5f8da256", preferred=True, submodules=True
    )
    version("1.3.0", commit="729a9b2ec97a7e93cbc58213493f28ca11f08754")

    depends_on("cmake @3.10:", type=("build"))
