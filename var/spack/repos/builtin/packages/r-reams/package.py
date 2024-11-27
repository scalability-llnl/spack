# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReams(RPackage):
    """Resampling-Based Adaptive Model Selection.

    Resampling methods for adaptive linear model selection.  These can be
    thought of as extensions of the Akaike information criterion that account
    for searching among candidate models."""

    cran = "reams"

    version("0.1", sha256="ac24ea875b24bd18152afd87538b1f807f442cf2bd1c6ac1a365cf543c88181e")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-leaps", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"))
