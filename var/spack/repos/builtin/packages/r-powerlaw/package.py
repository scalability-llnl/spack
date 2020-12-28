# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPowerlaw(RPackage):
    """An implementation of maximum likelihood estimators for a variety of
       heavy tailed distributions, including both the discrete and continuous
       power law distributions. Additionally, a goodness-of-fit based approach
       is used to estimate the lower cut-off for the scaling region."""

    homepage = "https://github.com/csgillespie/poweRlaw"
    url      = "https://cloud.r-project.org/src/contrib/poweRlaw_0.70.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/poweRlaw"

    version('0.70.2', sha256='240f1454389b1a00ad483fb63e5b53243cc9367f21a3e7253ab2c293673459ab')
    version('0.70.1', sha256='15b1b8dadeb550c01b9f1308cfa64720be6fbf56afb80f6a096987d6a0055913')

    depends_on('r@3.1.0:', when='@:0.70.1', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@0.70.2:', type=('build', 'run'))
    depends_on('r-vgam', type=('build', 'run'))
