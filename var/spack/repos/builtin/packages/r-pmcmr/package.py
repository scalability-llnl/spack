# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPmcmr(RPackage):
    """Calculate Pairwise Multiple Comparisons of Mean Rank Sums.

    Note, that the 'PMCMR' package is superset by the novel 'PMCMRplus'
    package. The 'PMCMRplus' package contains all functions from  'PMCMR' and
    many more parametric and non-parametric multiple comparison procedures,
    one-factorial trend tests, as well as improved method functions,  such as
    print, summary and plot.  The 'PMCMR' package is no longer maintained, but
    kept for compatibility of reverse depending packages for some time."""

    cran = "PMCMR"

    version("4.4", sha256="e7b4d9d595a879a62c9b3bb44c1f95432ad75a6607f84ce6bfc6395fee1dc116")
    version("4.3", sha256="328a2880dd614dc412e8dca21d29ed9d5eea29ccbe0eff98c8068100856c7b25")
    version("4.1", sha256="6c164e2976c59ddd27297433a34fa61b1e70b9e26265abdf9c8af1b639d2d555")

    depends_on("r@3.0.0:", type=("build", "run"))
