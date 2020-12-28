# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRhdf5(RPackage):
    """R Interface to HDF5.

       This package provides an interface between HDF5 and R. HDF5's main
       features are the ability to store and access very large and/or complex
       datasets and a wide variety of metadata on mass storage (disk) through a
       completely portable file format. The rhdf5 package is thus suited for
       the exchange of large and/or complex datasets between R and other
       software package, and for letting R applications work on datasets that
       are larger than the available RAM."""

    homepage = "https://bioconductor.org/packages/rhdf5"
    git      = "https://git.bioconductor.org/packages/rhdf5.git"

    version('2.28.1', commit='e230fa34d6f3e97dd4e6065115675baf5e8213bb')
    version('2.26.2', commit='81e11258db493661a19cf83e142b690ecac4e6cf')
    version('2.24.0', commit='e926e8ce4e77082781afb943324a1e6745385b48')
    version('2.22.0', commit='4431bdc0a2bcbb8086ee08a0f2300129b808d1be')
    version('2.20.0', commit='37b5165325062728bbec9167f89f5f4b794f30bc')

    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('r-rhdf5lib', when='@2.24.0:', type=('build', 'run'))

    depends_on('r@3.5.0:', when='@2.26.2:', type=('build', 'run'))
    depends_on('r-rhdf5lib@1.3.2:', when='@2.26.2:', type=('build', 'run'))

    depends_on('gmake', type='build')
