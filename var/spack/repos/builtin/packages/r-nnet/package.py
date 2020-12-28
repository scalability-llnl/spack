# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNnet(RPackage):
    """Software for feed-forward neural networks with a single hidden layer,
    and for multinomial log-linear models."""

    homepage = "http://www.stats.ox.ac.uk/pub/MASS4/"
    url      = "https://cloud.r-project.org/src/contrib/nnet_7.3-12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nnet"

    version('7.3-12', sha256='2723523e8581cc0e2215435ac773033577a16087a3f41d111757dd96b8c5559d')

    depends_on('r@2.14:', type=('build', 'run'))
