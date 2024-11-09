# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Capstone(CMakePackage):
    """Capstone is a lightweight multi-platform,
    multi-architecture disassembly framework."""

    homepage = "https://www.capstone-engine.org/"
    url = "https://github.com/capstone-engine/capstone/archive/4.0.1.tar.gz"
    git = "https://github.com/capstone-engine/capstone.git"

    license("BSD-3-Clause-Clear")

    version("next", branch="next")
    version("5.0.1", sha256="2b9c66915923fdc42e0e32e2a9d7d83d3534a45bb235e163a70047951890c01a")
    version("4.0.2", sha256="7c81d798022f81e7507f1a60d6817f63aa76e489aa4e7055255f21a22f5e526a")
    version("4.0.1", sha256="79bbea8dbe466bd7d051e037db5961fdb34f67c9fac5c3471dd105cfb1e05dc7")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def cmake_args(self):
        return ["-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=TRUE"]
