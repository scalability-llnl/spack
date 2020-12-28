# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4reporting(RPackage):
    """Automated Affymetrix Array Analysis Reporting Package."""

    homepage = "https://bioconductor.org/packages/a4Reporting"
    git      = "https://git.bioconductor.org/packages/a4Reporting.git"

    version('1.32.0', commit='8d781899c625892080eb50f322694dd640d5f792')
    version('1.30.0', commit='ae9b9ade45cfac2636d0445a7e0a029dfe3b9390')
    version('1.28.0', commit='0fe72f48374353c39479a45e5516d0709f8c9ef7')
    version('1.26.0', commit='cce201502e2d3b28fd2823b66d9f81b034dc7eaa')
    version('1.24.0', commit='bf22c4d50daf40fc9eaf8c476385bf4a24a5b5ce')

    depends_on('r-annaffy', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
