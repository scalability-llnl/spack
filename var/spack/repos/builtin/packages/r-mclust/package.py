# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMclust(RPackage):
    """mclust: Gaussian Mixture Modelling for Model-Based Clustering,
    Classification, and Density Estimation"""

    homepage = "http://www.stat.washington.edu/mclust"
    url      = "https://cran.r-project.org/src/contrib/mclust_5.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mclust"

    version('5.4.4', sha256='ccc31b0ad445e121a447b04988e73232a085c506fcc7ebdf11a3e0754aae3e0d')
    version('5.3', '74aac9fccdfc78373ce733c1a09176ef')

    depends_on('r@3.0.0:')
