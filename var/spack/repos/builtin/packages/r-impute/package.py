# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RImpute(RPackage):
    """impute: Imputation for microarray data.

       Imputation for microarray data (currently KNN only)"""

    homepage = "https://bioconductor.org/packages/impute"
    git      = "https://git.bioconductor.org/packages/impute.git"

    version('1.58.0', commit='dc17173df08d965a0d0aac9fa4ad519bd99d127e')
    version('1.56.0', commit='6c037ed4dffabafceae684265f86f2a18751b559')
    version('1.54.0', commit='efc61f5197e8c4baf4ae881fb556f0312beaabd8')
    version('1.52.0', commit='7fa1b917a5dd60f2aaf52d9aae1fcd2c93511d63')
    version('1.50.1', commit='31d1cc141797afdc83743e1d95aab8a90ee19b71')

    depends_on('r@2.10:', type=('build', 'run'))
