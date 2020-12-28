# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomfields(RPackage):
    """Methods for the inference on and the simulation of Gaussian fields
       are provided, as well as methods for the simulation of extreme
       value random fields."""

    homepage = "https://cloud.r-project.org/package=RandomFields"
    url      = "https://cloud.r-project.org/src/contrib/RandomFields_3.1.50.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RandomFields"

    version('3.3.6', sha256='51b7bfb4e5bd7fd0ce1207c77f428508a6cd3dfc9de01545a8724dfd9c050213')
    version('3.3.4', sha256='a340d4f3ba7950d62acdfa19b9724c82e439d7b1a9f73340124038b7c90c73d4')
    version('3.1.50', sha256='2d6a07c3a716ce20f9c685deb59e8fcc64fd52c8a50b0f04baf451b6b928e848')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-randomfieldsutils@0.5.1:', type=('build', 'run'))
