# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LanlCmakeModules(CMakePackage):
    """CMake modules for projects that have not yet adopted modern CMake."""

    maintainers("tuxfan")
    homepage = "https://lanl.github.io/cmake-modules"
    git = "https://github.com/lanl/cmake-modules.git"

    version("develop", branch="develop")
