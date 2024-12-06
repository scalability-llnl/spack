# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomglm(RPackage):
    """Random General Linear Model Prediction.

    The package implements a bagging predictor based on general linear
    models."""

    cran = "randomGLM"

    version("1.10-1", sha256="df324edf0c69926da1a3991dff10714ca4ec7a271d091a0a09d2a6a1d86da714")
    version("1.02-1", sha256="3bf7c1dbdacc68125f8ae3014b9bc546dd3328d04ad015d154781bdf3f1a230c")

    depends_on("r@2.14.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.10-1:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-hmisc", type=("build", "run"), when="@1.10-1:")
    depends_on("r-geometry", type=("build", "run"), when="@1.10-1:")
    depends_on("r-survival", type=("build", "run"), when="@1.10-1:")
    depends_on("r-matrixstats", type=("build", "run"), when="@1.10-1:")
