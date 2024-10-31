# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fpzip(CMakePackage):
    """fpzip compressor"""

    homepage = "https://github.com/llnl/fpzip"
    url = "https://github.com/LLNL/fpzip/releases/download/1.3.0/fpzip-1.3.0.tar.gz"
    git = "https://github.com/llnl/fpzip"

    maintainers("robertu94")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.3.0", sha256="248df7d84259e3feaa4c4797956b2a77c3fcd734e8f8fdc51ce171dcf4f0136c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
