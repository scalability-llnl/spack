# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInteractivedisplaybase(RPackage):
    """Base package for enabling powerful shiny web displays of Bioconductor
       objects.

       The interactiveDisplayBase package contains the the basic methods needed
       to generate interactive Shiny based display methods for Bioconductor
       objects."""

    homepage = "https://bioconductor.org/packages/interactiveDisplayBase"
    git      = "https://git.bioconductor.org/packages/interactiveDisplayBase.git"

    version('1.22.0', commit='4ce3cde1dabc01375c153ad614d77a5e28b96916')
    version('1.20.0', commit='f40912c8af7afbaaf68c003a6e148d81cbe84df6')
    version('1.18.0', commit='d07ea72a595877f27bf054f664f23e8f0304def8')
    version('1.16.0', commit='a86aa586b589497f5449d36c2ce67a6b6055026d')
    version('1.14.0', commit='e2ccc7eefdd904e3b1032dc6b3f4a28d08c1cd40')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
