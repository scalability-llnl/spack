# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mitos(CMakePackage):
    """Mitos is a library and a tool for collecting sampled memory
    performance data to view with MemAxes"""

    homepage = "https://github.com/llnl/Mitos"
    url = "https://github.com/LLNL/Mitos/archive/v0.9.1.tar.gz"
    git = "https://github.com/llnl/Mitos.git"

    license("LGPL-2.1-or-later")

    version("0.9.2", commit="8cb143a2e8c00353ff531a781a9ca0992b0aaa3d")
    version("0.9.1", sha256="67abe227d2f9b4d2f235031b526d3ceb2c4792ad98772b1b1d5af0d227a795fc")

    depends_on("cxx", type="build")  # generated

    depends_on("dyninst@8.2.1:")
    depends_on("hwloc")
    depends_on("mpi")
    depends_on("cmake@2.8:", type="build")
