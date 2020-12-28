# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLaplacesdemon(RPackage):
    """Provides a complete environment for Bayesian inference using a variety
       of different samplers (see ?LaplacesDemon for an overview). The README
       describes the history of the package development process."""

    homepage = "https://github.com/LaplacesDemonR/LaplacesDemon"
    url      = "https://cloud.r-project.org/src/contrib/LaplacesDemon_16.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/LaplacesDemon"

    version('16.1.1', sha256='779ed1dbfed523a15701b4d5d891d4f1f11ab27518826a8a7725807d4c42bd77')
    version('16.1.0', sha256='41d99261e8fc33c977b43ecf66ebed8ef1c84d9bd46b271609e9aadddc2ca8bb')
    version('16.0.1', sha256='be21eff3c821b4fe0b4724f03c9221c2456257f93d91f864de11e95dc35e8679')

    depends_on('r@3.0.0:', type=('build', 'run'))
