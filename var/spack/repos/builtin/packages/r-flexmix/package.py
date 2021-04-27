# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFlexmix(RPackage):
    """Flexible Mixture Modeling

    A general framework for finite mixtures of regression models using the EM
    algorithm is implemented. The E-step and all data handling are provided,
    while the M-step can be supplied by the user to easily define new models.
    Existing drivers implement mixtures of standard linear models, generalized
    linear models and model-based clustering."""

    homepage = "https://cloud.r-project.org/package=flexmix"
    url      = "https://cloud.r-project.org/src/contrib/flexmix_2.3-14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/flexmix"

    version('2.3-17', sha256='36019b7833032409ac61720dd625fa5a581a1d8bcba9045b04979c90907b5649')
    version('2.3-15', sha256='ba444c0bfe33ab87d440ab590c06b03605710acd75811c1622253171bb123f43')
    version('2.3-14', sha256='837c7f175a211b3c484b2c7b81ec9729889a614c5c6e7d70c95a2c1d60ff846a')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-modeltools@0.2-16:', type=('build', 'run'))
    depends_on('r-nnet', type=('build', 'run'))
