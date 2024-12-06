# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AdeptUtils(CMakePackage):
    """Utility libraries for LLNL performance tools."""

    homepage = "https://github.com/llnl/adept-utils"
    url = "https://github.com/llnl/adept-utils/archive/v1.0.tar.gz"

    version("1.0.1", sha256="259f777aeb368ede3583d3617bb779f0fde778319bf2122fdd216bdf223c015e")
    version("1.0", sha256="fed29366c9bcf5f3799220ae3b351d2cb338e2aa42133d61584ea650aa8d6ff7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@:1.72.0")
    depends_on("mpi")
    depends_on("cmake@2.8:", type="build")
