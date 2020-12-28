# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRtsne(RPackage):
    """An R wrapper around the fast T-distributed Stochastic Neighbor
    Embedding implementation."""

    homepage = "https://cloud.r-project.org/package=Rtsne"
    url      = "https://cloud.r-project.org/src/contrib/Rtsne_0.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rtsne"

    version('0.15', sha256='56376e4f0a382fad3d3d40e2cb0562224be5265b827622bcd235e8fc63df276c')
    version('0.13', sha256='1c3bffe3bd11733ee4fe01749c293669daafda1af2ec74f9158f6080625b999d')
    version('0.11', sha256='1e2e7368f3de870b9270f70b207ba9e8feea67f9b061cb6abb2fec785fb7247e')
    version('0.10', sha256='c54371f4a935520e7e7ab938ef8f5f7f9ad2a829123b9513ae715c07de034790')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
