# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSquarem(RPackage):
    """Algorithms for accelerating the convergence of slow, monotone sequences
    from smooth, contraction mapping such as the EM algorithm. It can be used
    to accelerate any smooth, linearly convergent acceleration scheme. A
    tutorial style introduction to this package is available in a vignette on
    the CRAN download page or, when the package is loaded in an R session, with
    vignette("SQUAREM")."""

    homepage = "http://www.jhsph.edu/agingandhealth/People/Faculty_personal_pages/Varadhan.html"
    url      = "https://cloud.r-project.org/src/contrib/SQUAREM_2017.10-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/SQUAREM"

    version('2017.10-1', sha256='9b89905b436f1cf3faa9e3dabc585a76299e729e85ca659bfddb4b7cba11b283')

    depends_on('r@3.0:', type=('build', 'run'))
