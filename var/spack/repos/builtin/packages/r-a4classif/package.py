# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4classif(RPackage):
    """Automated Affymetrix Array Analysis Classification Package.

       Automated Affymetrix Array Analysis Classification Package"""

    homepage = "https://bioconductor.org/packages/a4Classif"
    git      = "https://git.bioconductor.org/packages/a4Classif.git"

    version('1.32.0', commit='aa4f22df2da54b71e1a238d2b9cbcb3afa6f7f88')
    version('1.30.0', commit='b62841bff2f8894a3011a4e74afc37076d1322a3')
    version('1.28.0', commit='3464011f6c3ddb41b78acc47e775539034287be7')
    version('1.26.0', commit='bc4018c3c441e1840bb3e2959c07611489439a50')
    version('1.24.0', commit='ca06bf274c87a73fc12c29a6eea4b90289fe30b1')

    depends_on('r-a4core', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-a4preproc', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-glmnet', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-mlinterfaces', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-pamr', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-rocr', when='@1.24.0:', type=('build', 'run'))
    depends_on('r-varselrf', when='@1.24.0:', type=('build', 'run'))
