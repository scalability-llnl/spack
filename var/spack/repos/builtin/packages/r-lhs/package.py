# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLhs(RPackage):
    """Provides a number of methods for creating and augmenting Latin Hypercube
       Samples."""

    homepage = "http://lhs.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/lhs_0.16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lhs"

    version('1.0', sha256='38c53482b360bdea89ddcfadf6d45476c80b99aee8902f97c5e97975903e2745')
    version('0.16', '088e593e5283414951e7e541a50ec2d1')

    depends_on('r@3.4.0:')
    depends_on('r-rcpp', when='@1.0:', type=('build', 'run'))
