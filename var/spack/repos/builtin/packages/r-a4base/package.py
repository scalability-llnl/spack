# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4base(RPackage):
    """Automated Affymetrix Array Analysis Base Package."""

    homepage = "https://bioconductor.org/packages/a4Base"
    git      = "https://git.bioconductor.org/packages/a4Base.git"

    version('1.32.0', commit='8a1e15d25494c54db8c1de5dbbd69e628569e3d7')
    version('1.30.0', commit='fc370b2bd8286acc1e42a10344d91974f5b94229')
    version('1.28.0', commit='3918a9ebafa065027c29620ee4d83789cb02f932')
    version('1.26.0', commit='9b8ee4a8be90f5035a4b105ecebb8bb5b50cd0d9')
    version('1.24.0', commit='f674afe424a508df2c8ee6c87a06fbd4aa410ef6')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annaffy', type=('build', 'run'))
    depends_on('r-mpm', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-a4preproc', type=('build', 'run'))
    depends_on('r-a4core', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
