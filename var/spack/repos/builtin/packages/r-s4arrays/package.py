# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RS4arrays(RPackage):
    """Foundation of array-like containers in Bioconductor."""

    bioc = "S4Arrays"

    version("1.6.0", commit="e100af0de22e3b49ce3b544c158eb327b1bd2133")
    version("1.4.1", commit="472c245dc1c66c4eb0877b081e4a95f8eff97ba8")
    version("1.2.1", commit="59b8f4e28d2273145411f0d5429d1f31f6b79e12")

    depends_on("r@4.3.0:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-biocgenerics@0.45.2:", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
