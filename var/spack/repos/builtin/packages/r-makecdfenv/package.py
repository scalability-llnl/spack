# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMakecdfenv(RPackage):
    """CDF Environment Maker.

       This package has two functions. One reads a Affymetrix chip description
       file (CDF) and creates a hash table environment containing the
       location/probe set membership mapping. The other creates a package that
       automatically loads that environment."""

    homepage = "https://bioconductor.org/packages/makecdfenv"
    git      = "https://git.bioconductor.org/packages/makecdfenv.git"

    version('1.60.0', commit='900ece3ecd7a0ade9f8a0374e5a03def4e079cb3')
    version('1.58.0', commit='6f513e39c4920a6da10d22718fc3bf278fe5ffe2')
    version('1.56.0', commit='f6b48e9a9f18598653d05bc0bdffeae7fefbb327')
    version('1.54.0', commit='3ff646ddc4b028e46b1e091ff9c2d17ce77cec26')
    version('1.52.0', commit='b88a3e93e3b7feeeca69eda7c1fc5a0826c81120')

    depends_on('r@2.6.0:', type=('build', 'run'))
    depends_on('r-affyio', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
