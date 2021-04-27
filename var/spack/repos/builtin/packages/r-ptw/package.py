# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPtw(RPackage):
    """Parametric Time Warping

    Parametric Time Warping aligns patterns, i.e. it aims to put corresponding
    features at the same locations. The algorithm searches for an optimal
    polynomial describing the warping. It is possible to align one sample to a
    reference, several samples to the same reference, or several samples to
    several references. One can choose between calculating individual warpings,
    or one global warping for a set of samples and one reference. Two
    optimization criteria are implemented: RMS (Root Mean Square error) and WCC
    (Weighted Cross Correlation). Both warping of peak profiles and of peak
    lists are supported. A vignette for the latter is contained in the inst/doc
    directory of the source package - the vignette source can be found on the
    package github site."""

    homepage = "https://cloud.r-project.org/package=ptw"
    url      = "https://cloud.r-project.org/src/contrib/ptw_1.9-12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ptw"

    version('1.9-15', sha256='22fa003f280bc000f46bca88d69bf332b29bc68435115ba8044533b70bfb7b46')
    version('1.9-13', sha256='7855e74a167db3d3eba9df9d9c3daa25d7cf487cbcfe8b095f16d96eba862f46')
    version('1.9-12', sha256='cdb1752e04e661e379f11867b0a17e2177e9ee647c54bbcc37d39d6b8c062b84')

    depends_on('r-nloptr', type=('build', 'run'))
