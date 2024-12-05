# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Crunch(CMakePackage):
    """Advanced DXTc texture compression and transcoding library."""

    homepage = "https://github.com/BinomialLLC/crunch"
    # The original repo does not have any build system or installation instructions. This package
    # was added primarily as a possible dependency of GDAL. The following fork was created by the
    # maintainer of GDAL and includes several additional commits to add a CMake build system and
    # fix compilation bugs. If these commits are ever merged into upstream, we can switch to that.
    git = "https://github.com/rouault/crunch.git"

    license("Zlib")

    # No stable releases since 2012
    version("master", branch="build_fixes")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.5:", type="build")

    conflicts("platform=darwin")
