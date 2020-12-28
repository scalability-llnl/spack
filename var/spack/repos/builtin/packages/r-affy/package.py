# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffy(RPackage):
    """Methods for Affymetrix Oligonucleotide Arrays.

       The package contains functions for exploratory oligonucleotide array
       analysis. The dependence on tkWidgets only concerns few convenience
       functions. 'affy' is fully functional without it."""

    homepage = "https://bioconductor.org/packages/affy"
    git      = "https://git.bioconductor.org/packages/affy.git"

    version('1.62.0', commit='097ab4aa98a1700c5fae65d07bed44a477714605')
    version('1.60.0', commit='fcae363e58b322ad53584d9e15e80fa2f9d17206')
    version('1.58.0', commit='4698231f45f225228f56c0708cd477ad450b4ee6')
    version('1.56.0', commit='d36a7b8f05b1ef60162d94e75037d45c48f88871')
    version('1.54.0', commit='a815f02906fcf491b28ed0a356d6fce95a6bd20e')

    depends_on('r@2.8.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.1.12:', type=('build', 'run'))
    depends_on('r-biobase@2.5.5:', type=('build', 'run'))
    depends_on('r-affyio@1.13.3:', type=('build', 'run'))
    depends_on('r-biocinstaller', when='@1.54.0:1.58.0', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))

    depends_on('r-biocmanager', when='@1.60.0:', type=('build', 'run'))
