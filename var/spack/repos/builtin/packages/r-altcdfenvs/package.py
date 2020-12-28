# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAltcdfenvs(RPackage):
    """alternative CDF environments (aka probeset mappings).

       Convenience data structures and functions to handle cdfenvs"""

    homepage = "https://bioconductor.org/packages/altcdfenvs"
    git      = "https://git.bioconductor.org/packages/altcdfenvs.git"

    version('2.46.0', commit='90a11e748a5af98cabfd6670a5b7b256420d172b')
    version('2.44.0', commit='d804f6432422bd532abab415710f890b36cc8133')
    version('2.42.0', commit='00ec6461877a063d938494b8ed0cd273a3b20b85')
    version('2.40.0', commit='517a208f49f168bdd3cde40ed216282c417237d7')
    version('2.38.0', commit='2e92b9da76dbe50af4bf33c525134e29e9809291')

    depends_on('r@2.7:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.1.0:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.25:', type=('build', 'run'))
    depends_on('r-biobase@2.15.1:', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-makecdfenv', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r-hypergraph', type=('build', 'run'))
