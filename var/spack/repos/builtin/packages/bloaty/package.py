# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bloaty(CMakePackage):
    """Bloaty McBloatface: a size profiler for binaries."""

    homepage = "https://github.com/google/bloaty"
    url = "https://github.com/google/bloaty/releases/download/v1.1/bloaty-1.1.tar.bz2"

    maintiners = ["cyrush"]

    license("Apache-2.0")

    version("1.1", sha256="a308d8369d5812aba45982e55e7c3db2ea4780b7496a5455792fb3dcba9abd6f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
