# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RKernsmooth(RPackage):
    """Functions for kernel smoothing (and density estimation)

    Functions for kernel smoothing (and density estimation) corresponding to
    the book:  Wand, M.P. and Jones, M.C. (1995) "Kernel Smoothing"."""

    homepage = "https://cloud.r-project.org/package=KernSmooth"
    url      = "https://cloud.r-project.org/src/contrib/KernSmooth_2.23-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/KernSmooth"

    version('2.23-18', sha256='8334800c5ad2305539d2731b929ea34f50fa4269ba87277b699fd5be5b03c490')
    version('2.23-15', sha256='8b72d23ed121a54af188b2cda4441e3ce2646359309885f6455b82c0275210f6')

    depends_on('r@2.5.0:', type=('build', 'run'))
