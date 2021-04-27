# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMda(RPackage):
    """Mixture and Flexible Discriminant Analysis

    Mixture and flexible discriminant analysis, multivariate adaptive
    regression splines (MARS), BRUTO."""

    homepage = "https://cloud.r-project.org/package=mda"
    url      = "https://cloud.r-project.org/src/contrib/mda_0.4-9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mda"

    version('0.5-2', sha256='344f2053215ddf535d1554b4539e9b09067dac878887cc3eb995cef421fc00c3')
    version('0.4-10', sha256='7036bc622a8fea5b2de94fc19e6b64f5f0c27e5d743ae7646e116af08c9de6a5')
    version('0.4-9', sha256='b72456d2fa5b49895644489735d21cf4836d3d597f5e693e6103cce1887ffd85')

    depends_on('r@1.9.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@0.5-2:', type=('build', 'run'))
    depends_on('r-class', type=('build', 'run'))
