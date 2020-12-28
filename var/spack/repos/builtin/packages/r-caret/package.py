# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaret(RPackage):
    """Misc functions for training and plotting classification and regression
    models."""

    homepage = "https://github.com/topepo/caret/"
    url      = "https://cloud.r-project.org/src/contrib/caret_6.0-73.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/caret"

    version('6.0-84', sha256='a1831c086a9c71b469f7405649ba04517683cdf229e119c005189cf57244090d')
    version('6.0-83', sha256='9bde5e4da1f0b690bfe06c2439c0136504e851a8d360bf56b644f171fe20dcef')
    version('6.0-73', sha256='90a0a4a10f1a3b37502cb0ed7d8830063d059a548faabb9cc5d8d34736c7eacb')
    version('6.0-70', sha256='21c5bdf7cf07bece38729465366564d8ca104c2466ee9fd800ca1fd88eb82f38')

    depends_on('r@2.10:', when='@:6.0-81', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@6.0-82:', type=('build', 'run'))
    depends_on('r-lattice@0.20:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-car', when='@:6.0-73', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-modelmetrics@1.1.0:', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-recipes@0.1.4:', when='@6.0-83:', type=('build', 'run'))
    depends_on('r-withr@2.0.0:', when='@6.0-83:', type=('build', 'run'))
