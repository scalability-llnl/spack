# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Byfl(CMakePackage):
    """Compiler-based Application Analysis"""

    homepage = "https://github.com/lanl/Byfl"
    url = "https://github.com/lanl/Byfl/archive/refs/tags/v1.8.0.tar.gz"

    maintainers("spakin", "ltang85")

    license("BSD-3-Clause")

    version("1.8.0", sha256="45a9640ba2d77153a425c72349c18b124754123b30c411707b71abd217bbfce0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # llvm-13 builds, but doesn’t work
    depends_on("llvm@:12.9999")
