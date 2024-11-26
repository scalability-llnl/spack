# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mgardx(CMakePackage):
    """MGARD implementation for research purposes
    forked from: https://github.com/lxAltria/MGARDx"""

    # Some of the functionality of this compressor were moved to `MGARD` proper
    # effectively retiring this package.  This package lives on to access some of
    # this functionality.  Includes minor patches to support spack.

    homepage = "https://github.com/lxAltria/MGARDx"
    git = "https://github.com/robertu94/MGARDx"

    maintainers("robertu94")

    variant("shared", description="build shared libraries", default=True)

    version("2022-01-27", commit="aabe9de1a331eaeb8eec41125dd45e30c1d03af4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("sz-cpp")
    depends_on("pkgconfig")
    depends_on("zstd")

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        return args
