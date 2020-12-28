# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycomp(RPackage):
    """Graphics Toolbox for Assessment of Affymetrix Expression Measures.

       The package contains functions that can be used to compare expression
       measures for Affymetrix Oligonucleotide Arrays."""

    homepage = "https://bioconductor.org/packages/affycomp"
    git      = "https://git.bioconductor.org/packages/affycomp.git"

    version('1.60.0', commit='5dbe61fa04941529a0fc70b728021c8e00c4ba0c')
    version('1.58.0', commit='99607b2c4aad37e3e63eccbd12d0d533762f28ef')
    version('1.56.0', commit='b0994da338be19396e647c680059fd35341b50a2')
    version('1.54.0', commit='65281c1ca37147c2a54ad3722a8d5ff0ffa5acc5')
    version('1.52.0', commit='1b97a1cb21ec93bf1e5c88d5d55b988059612790')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-biobase@2.3.3:', type=('build', 'run'))
