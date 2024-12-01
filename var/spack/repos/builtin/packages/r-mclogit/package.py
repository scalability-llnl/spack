# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMclogit(RPackage):
    """Multinomial Logit Models, with or without Random Effects or
    Overdispersion.

    Provides estimators for multinomial logit models in their conditional logit
    and baseline logit variants, with or without random effects, with or
    without overdispersion. Random effects models are estimated using the PQL
    technique (based on a Laplace approximation) or the MQL technique (based on
    a Solomon-Cox approximation). Estimates should be treated with caution if
    the group sizes are small."""

    cran = "mclogit"

    license("GPL-2.0-only")

    version("0.9.6", sha256="9adc5f6d8649960abe009c30d9b4c448ff7d174c455a594cbf104a33d5a36f69")

    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-memisc", type=("build", "run"))
