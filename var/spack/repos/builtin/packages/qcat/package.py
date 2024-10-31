# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qcat(CMakePackage):
    """Quick data compression quality analysis tool"""

    homepage = "https://github.com/szcompressor/qcat"
    git = "https://github.com/szcompressor/qcat"

    maintainers("disheng222", "robertu94")

    license("BSD-2-Clause")

    version("master", branch="master")
    version("1.4", commit="f16032cf237837b1d32dde0c3daa6ad1ca4a912f")

    depends_on("c", type="build")  # generated

    depends_on("zstd")

    def cmake_args(self):
        args = ["-DQCAT_USE_BUNDLES=OFF"]
        return args
