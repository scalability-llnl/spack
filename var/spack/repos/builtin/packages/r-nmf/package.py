# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNmf(RPackage):
    """Algorithms and Framework for Nonnegative Matrix Factorization (NMF).

    Provides a framework to perform Non-negative Matrix Factorization (NMF).
    The package implements a set of already published algorithms and seeding
    methods, and provides a framework to test, develop and plug new/custom
    algorithms. Most of the built-in algorithms have been optimized in C++, and
    the main interface function provides an easy way of performing parallel
    computations on multicore machines."""

    cran = "NMF"

    version("0.27", sha256="af4302efca4a7654fecd31c376f1bb3496428279a50b8d5691c8a7e66e3f3ef9")
    version("0.26", sha256="8d44562ef5f33f3811929f944c9d029ec25526d2ddddfe7c8a5b6e23adbc2ec0")
    version("0.24.0", sha256="481811d35b3bbc07e9a60e2f853b05ef26581b43be9c6c4bab81151b8dcadd93")
    version("0.23.0", sha256="0f0cca01b37bf46fce90d2e951df609d3d377908aa607825083fd0c47cc24753")
    version("0.21.0", sha256="3b30c81c66066fab4a63c5611a0313418b840d8b63414db31ef0e932872d02e3")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-registry", type=("build", "run"))
    depends_on("r-rngtools@1.2.3:", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-stringr@1.0.0:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-gridbase", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-rcolorbrewer", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@0.23.0:")
    depends_on("r-biobase", type=("build", "run"), when="@0.23.0:")
    depends_on("r-codetools", type=("build", "run"), when="@0.26:")
    depends_on("r-pkgmaker@0.20:", type=("build", "run"), when="@:0.24.0")
