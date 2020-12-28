# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKernsmooth(RPackage):
    """Functions for kernel smoothing (and density estimation)."""

    homepage = "https://cloud.r-project.org/package=KernSmooth"
    url      = "https://cloud.r-project.org/src/contrib/KernSmooth_2.23-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/KernSmooth"

    version('2.23-15', sha256='8b72d23ed121a54af188b2cda4441e3ce2646359309885f6455b82c0275210f6')

    depends_on('r@2.5.0:', type=('build', 'run'))
