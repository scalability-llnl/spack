# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtlx(CMakePackage):
    """tlx is a collection of C++ helpers and extensions universally needed,
    but not found in the STL.
    The most important design goals and conventions are:
    1) high modularity with as little dependencies between
       modules as possible.
    2) attempt to never break existing interfaces.
    3) compile on all platforms with C++ - smartphones, supercomputers,
       windows, etc.
    4) zero external dependencies: no additional libraries are required.
    5) warning and bug-freeness on all compilers.
    6) keep overhead down - small overall size such that is can be included
       without bloating applications."""

    homepage = "https://tlx.github.io/"
    url = "https://github.com/tlx/tlx/archive/v0.5.20191212.tar.gz"

    maintainers("fabratu")

    license("BSL-1.0")

    version("0.6.1", sha256="24dd1acf36dd43b8e0414420e3f9adc2e6bb0e75047e872a06167961aedad769")
    version(
        "0.5.20200222", sha256="99e63691af3ada066682243f3a65cd6eb32700071cdd6cfedb18777b5ff5ff4d"
    )
    version(
        "0.5.20191212", sha256="5e67d3042a390dbb831b6d46437e3c7fadf738bff362aa7376b210b10ecd532d"
    )

    depends_on("cxx", type="build")  # generated
