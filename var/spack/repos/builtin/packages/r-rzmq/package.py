# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRzmq(RPackage):
    """Interface to the ZeroMQ lightweight messaging kernel."""

    homepage = "http://github.com/armstrtw/rzmq"
    url      = "https://cloud.r-project.org/src/contrib/rzmq_0.7.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rzmq"

    version('0.9.6', sha256='80a3fc6eb6f7851224c4cd5e219ca4db0286551ad429359d4df853ccb9234316')
    version('0.9.4', sha256='03fbda756d823c11fba359b94a6213c3440e61973331668eaac35779717f73ad')
    version('0.7.7', sha256='bdbaf77a0e04c5b6d6ce79ab2747848a5044355eed2e2c4d39c4ba16f97dc83d')

    depends_on('r@3.1.0:', when='@0.9.0:', type=('build', 'run'))
    depends_on('libzmq@3.0.0:')
