# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMclust(RPackage):
    """mclust: Gaussian Mixture Modelling for Model-Based Clustering,
    Classification, and Density Estimation"""

    homepage = "http://www.stat.washington.edu/mclust"
    url      = "https://cloud.r-project.org/src/contrib/mclust_5.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mclust"

    version('5.4.5', sha256='75f2963082669485953e4306ffa93db98335ee6afdc1318b95d605d56cb30a72')
    version('5.4.4', sha256='ccc31b0ad445e121a447b04988e73232a085c506fcc7ebdf11a3e0754aae3e0d')
    version('5.3', sha256='2b1b6d8266ae16b0e96f118df81559f208a568744a7c105af9f9abf1eef6ba40')

    depends_on('r@3.0.0:', type=('build', 'run'))
