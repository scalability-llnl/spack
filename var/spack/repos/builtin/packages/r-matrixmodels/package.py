# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatrixmodels(RPackage):
    """Modelling with sparse and dense 'Matrix' matrices, using modular
    prediction and response module classes."""

    homepage = "http://matrix.r-forge.r-project.org/"
    url      = "https://cloud.r-project.org/src/contrib/MatrixModels_0.4-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/MatrixModels"

    version('0.4-1', sha256='fe878e401e697992a480cd146421c3a10fa331f6b37a51bac83b5c1119dcce33')

    depends_on('r@3.0.1:', type=('build', 'run'))
    depends_on('r-matrix@1.1-5:', type=('build', 'run'))
