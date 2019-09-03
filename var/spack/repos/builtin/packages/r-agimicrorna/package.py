# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAgimicrorna(RPackage):
    """Processing and Differential Expression Analysis of Agilent microRNA
       chips

       Processing and Analysis of Agilent microRNA data"""

    homepage = "https://bioconductor.org/packages/AgiMicroRna"
    git      = "https://git.bioconductor.org/packages/AgiMicroRna.git"

    version('2.34.0', commit='aaa8cdd70ed2696c313f6240ffbfa044f0d97a7a')
    version('2.32.0', commit='681ae17d07e8e533f798a607b761b71a31f407d8')
    version('2.30.0', commit='99b5a8284cfe3e93c3ae85a2436e87101b9599dd')
    version('2.28.0', commit='62c4a12f1168c7aa1ab46d2c97090ef71478328e')
    version('2.26.0', commit='6dd74bae47986f2a23d03e3f1f9f78f701dd8053')

    depends_on('r@3.6.0:3.6.9', when='@2.34.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.32.0', type=('build', 'run'))
    depends_on('r@3.5.0:3.5.9', when='@2.30.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.28.0', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.26.0', type=('build', 'run'))

    depends_on('r-affy@1.22:', when='@2.26.0:', type=('build', 'run'))
    depends_on('r-affycoretools', when='@2.26.0:', type=('build', 'run'))
    depends_on('r-biobase', when='@2.26.0:', type=('build', 'run'))
    depends_on('r-limma', when='@2.26.0:', type=('build', 'run'))
    depends_on('r-preprocesscore', when='@2.26.0:', type=('build', 'run'))
