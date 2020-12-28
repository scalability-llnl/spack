# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNetwork(RPackage):
    """Tools to create and modify network objects. The network class can
       represent a range of relational data types, and supports
       arbitrary vertex/edge/graph attributes."""

    homepage = "https://statnet.org"
    url      = "https://cloud.r-project.org/src/contrib/network_1.13.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/network"

    version('1.15', sha256='5cbe5c0369e5f8363e33a86f14fd33ce8727166106381627ecd13b7452e14cb3')
    version('1.14-377', sha256='013c02f8d97f1f87f2c421760534df9353d2a8c2277f20b46b59fb79822d3e46')
    version('1.13.0', sha256='7a04ea89261cdf32ccb52222810699d5fca59a849053e306b5ec9dd5c1184f87')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-tibble', when='@1.14-377:', type=('build', 'run'))
    depends_on('r-magrittr', when='@1.14-377:', type=('build', 'run'))
