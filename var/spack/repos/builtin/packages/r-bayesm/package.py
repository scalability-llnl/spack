# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBayesm(RPackage):
    """Bayesian Inference for Marketing/Micro-Econometrics"""

    homepage = "https://cloud.r-project.org/package=bayesm"
    url      = "https://cloud.r-project.org/src/contrib/bayesm_3.1-0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bayesm"

    version('3.1-3', sha256='51e4827eca8cd4cf3626f3c2282543df7c392b3ffb843f4bfb386fe104642a10')
    version('3.1-2', sha256='a332f16e998ab10b17a2b1b9838d61660c36e914fe4d2e388a59f031d52ad736')
    version('3.1-1', sha256='4854517dec30ab7c994de862aae1998c2d0c5e71265fd9eb7ed36891d4676078')
    version('3.1-0.1', sha256='5879823b7fb6e6df0c0fe98faabc1044a4149bb65989062df4ade64e19d26411')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
    depends_on('r-rcpparmadillo', type=('build', 'run'))
