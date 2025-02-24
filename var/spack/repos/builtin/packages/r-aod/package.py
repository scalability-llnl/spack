# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAod(RPackage):
    """Analysis of Overdispersed Data.

    Provides a set of functions to analyse overdispersed counts or proportions.
    Most of the methods are already available elsewhere but are scattered in
    different packages. The proposed functions should be considered as
    complements to more sophisticated methods such as generalized estimating
    equations (GEE) or generalized linear mixed effect models (GLMM)."""

    cran = "aod"

    license("GPL-2.0-or-later")

    version("1.3.3", sha256="b7245e8abf7d78cdfa7f74f6d90f79a418b883058aa3edd5977a60bdbed4087e")
    version("1.3.2", sha256="9b85be7b12b31ac076f2456853a5b18d8a79ce2b86d00055264529a0cd28515c")
    version("1.3.1", sha256="052d8802500fcfdb3b37a8e3e6f3fbd5c3a54e48c3f68122402d2ea3a15403bc")

    depends_on("r@2.10:", type=("build", "run"))
