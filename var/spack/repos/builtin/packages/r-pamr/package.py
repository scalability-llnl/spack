# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPamr(RPackage):
    """Pam: Prediction Analysis for Microarrays

    Some functions for sample classification in microarrays."""

    cran = "pamr"

    license("GPL-2.0-only")

    version("1.57", sha256="01968f7620f1a5e4be1ce666f7ff52211b9dcf6cf5948112c7441aabae56af3d")
    version("1.56.1", sha256="d0e527f2336ee4beee91eefb2a8f0dfa96413d9b5a5841d6fc7ff821e67c9779")
    version("1.55", sha256="ed910194937a6097ec79234d84777856fd520b111a7c79f7c86dc607169cc3c3")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.57:")
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
