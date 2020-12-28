# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMnormt(RPackage):
    """Functions are provided for computing the density and the distribution
       function of multivariate normal and "t" random variables, and for
       generating random vectors sampled from these distributions.
       Probabilities are computed via non-Monte Carlo methods; different
       routines are used in the case d=1, d=2, d>2, if d denotes the number
       of dimensions."""

    homepage = "http://azzalini.stat.unipd.it/SW/Pkg-mnormt"
    url      = "https://cloud.r-project.org/src/contrib/mnormt_1.5-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mnormt"

    version('1.5-5', sha256='ff78d5f935278935f1814a69e5a913d93d6dd2ac1b5681ba86b30c6773ef64ac')

    depends_on('r@2.2.0:', type=('build', 'run'))
