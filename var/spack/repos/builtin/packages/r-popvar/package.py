# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPopvar(RPackage):
    """PopVar: Genomic Breeding Tools: Genetic Variance Prediction andCross-
       Validation"""

    homepage = "https://cloud.r-project.org/package=PopVar"
    url      = "https://cloud.r-project.org/src/contrib/PopVar_1.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PopVar"

    version('1.2.1', sha256='5e3df79634ab63708a431e4b8e6794675972ac6c58d2bc615726aa0f142f5f25')

    depends_on('r@3.1.1:', type=('build', 'run'))
    depends_on('r-bglr', type=('build', 'run'))
    depends_on('r-qtl', type=('build', 'run'))
    depends_on('r-rrblup', type=('build', 'run'))
