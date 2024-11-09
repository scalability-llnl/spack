# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Poorjit(CMakePackage):
    """A poorman's JIT library"""

    homepage = "https://github.com/robertu94/poorjit"
    url = "https://github.com/robertu94/poorjit/archive/refs/tags/0.0.2.tar.gz"
    git = "https://github.com/robertu94/poorjit"

    maintainers("robertu94")

    license("BSD-4-Clause", checked_by="robertu94")

    version("0.0.2", sha256="d7d43ba3b343ac8a6b0fb4928d5882f64a8c13c6fccfc37e1a3f3cd581c2739a")

    depends_on("cxx", type="build")  # generated

    depends_on("boost+filesystem")
    depends_on("zlib")
    depends_on("fmt")

    def cmake_args(self):
        args = []
        return args
