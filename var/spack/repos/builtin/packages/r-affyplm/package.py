# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyplm(RPackage):
    """Methods for fitting probe-level models.

       A package that extends and improves the functionality of the base affy
       package. Routines that make heavy use of compiled code for speed.
       Central focus is on implementation of methods for fitting probe-level
       models and tools using these models. PLM based quality assessment
       tools."""

    homepage = "https://bioconductor.org/packages/affyPLM"
    git      = "https://git.bioconductor.org/packages/affyPLM.git"

    version('1.60.0', commit='b11e377d6af3fd0f28aba8195ebf171003da1a9d')
    version('1.58.0', commit='32764c7691d9a72a301d50042a8844112887a1c8')
    version('1.56.0', commit='13dfc558281af9a177d4d592c34cf7ace629af0e')
    version('1.54.0', commit='09cf5f6e01dd2d0aae3e9ddab27301f04bfd645c')
    version('1.52.1', commit='e8613a6018c4ee58045df6bf19128844f50a1f43')

    depends_on('r@2.6.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.3.2:', type=('build', 'run'))
    depends_on('r-affy@1.11.0:', type=('build', 'run'))
    depends_on('r-biobase@2.17.8:', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-preprocesscore@1.5.1:', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
