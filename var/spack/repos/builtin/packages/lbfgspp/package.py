# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lbfgspp(CMakePackage):
    """A Header-only C++ Library for L-BFGS and L-BFGS-B Algorithms"""

    homepage = "https://lbfgspp.statr.me/"
    url = "https://github.com/yixuan/LBFGSpp/archive/refs/tags/v0.2.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="490720b9d5acce6459cb0336ca3ae0ffc48677225f0ebfb35c9bef6baefdfc6a")
    version("0.2.0", sha256="7101744a538c3aff52e10c82267305847b0b5e9d39f9974b4b29812cd1398ff9")

    depends_on("cxx", type="build")  # generated

    depends_on("eigen @3:")
