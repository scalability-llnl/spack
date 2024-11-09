# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Universal(CMakePackage):
    """Universal: a header-only C++ template library for universal number arithmetic"""

    homepage = "https://github.com/stillwater-sc/universal"
    url = "https://github.com/stillwater-sc/universal/archive/refs/tags/v3.68.tar.gz"

    maintainers("eschnett")

    license("MIT")

    version("3.68", sha256="67de4e0a3276b873a298ab98f1237ff3fd23240178e71405bf813ee38e4b1f62")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
