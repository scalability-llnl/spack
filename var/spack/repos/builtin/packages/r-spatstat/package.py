# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstat(RPackage):
    """Comprehensive open-source toolbox for
       analysing Spatial Point Patterns.
    """

    homepage = "https://cloud.r-project.org/package=spatstat"
    url      = "https://cloud.r-project.org/src/contrib/spatstat_1.64-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spatstat"

    version('1.64-1', sha256='ca3fc7d0d6b7a83fd045a7502bf03c6871fa1ab2cf411647c438fd99b4eb551a')
    version('1.63-3', sha256='07b4a1a1b37c91944f31779dd789598f4a5ad047a3de3e9ec2ca99b9e9565528')

    depends_on('r@3.3:', type=('build', 'run'))
    depends_on('r-rpart', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-spatstat-data@1.4-2:', type=('build', 'run'))
    depends_on('r-spatstat-utils@1.17:', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-deldir@0.0-21:', type=('build', 'run'))
    depends_on('r-abind', type=('build', 'run'))
    depends_on('r-tensor', type=('build', 'run'))
    depends_on('r-polyclip@1.10:', type=('build', 'run'))
    depends_on('r-goftest@1.2-2:', type=('build', 'run'))
