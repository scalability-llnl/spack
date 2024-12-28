# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSparsearray(RPackage):
    """High-performance sparse data representation and manipulation in R."""

    bioc = "SparseArray"

    version("1.7.2", commit="49e375d8e6d7d7a95aa3c7009d9f0fb199fd824f")

    depends_on("r@4.3.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.43.1:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrixgenerics@1.11.1:", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-s4arrays@1.5.11:", type=("build", "run"))
    depends_on("r-s4vectors@0.43.2:", type=("build", "run"))
    depends_on("r-xvector", type=("build", "run"))
