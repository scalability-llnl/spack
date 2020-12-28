# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLhs(RPackage):
    """Provides a number of methods for creating and augmenting Latin Hypercube
       Samples."""

    homepage = "http://lhs.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/lhs_0.16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lhs"

    version('1.0.1', sha256='a4d5ac0c6f585f2880364c867fa94e6554698beb65d3678ba5938dd84fc6ea53')
    version('1.0', sha256='38c53482b360bdea89ddcfadf6d45476c80b99aee8902f97c5e97975903e2745')
    version('0.16', sha256='9cd199c3b5b2be1736d585ef0fd39a00e31fc015a053333a7a319668d0809425')

    depends_on('r@3.3.0:', when='@:0.16', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@1.0:', type=('build', 'run'))
    depends_on('r-rcpp', when='@1.0:', type=('build', 'run'))
