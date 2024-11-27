# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastani(CMakePackage, AutotoolsPackage):
    """Fast, alignment-free computation of whole-genome Average Nucleotide
    Identity (ANI)"""

    homepage = "https://github.com/ParBLiSS/FastANI"
    url = "https://github.com/ParBLiSS/FastANI/archive/v1.33.tar.gz"
    maintainers("snehring")

    license("Apache-2.0")

    version("1.34", sha256="dc185cf29b9fa40cdcc2c83bb48150db46835e49b9b64a3dbff8bc4d0f631cb1")
    version("1.33", sha256="0b18b3074094722fb1b2247c1a1c4eb96295fff369b837f422e05072740e0013")

    depends_on("cxx", type="build")  # generated

    build_system(conditional("cmake", when="@1.34:"), "autotools", default="cmake")

    depends_on("autoconf", type="build", when="build_system=autotools")
    depends_on("automake", type="build", when="build_system=autotools")
    depends_on("cmake@3.20:", type="build", when="build_system=cmake")
    depends_on("libtool", type="build", when="build_system=autotools")
    depends_on("m4", type="build", when="build_system=autotools")
    depends_on("gsl", type=("build", "link"))
    depends_on("zlib-api", type=("build", "link"))
