# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hyphy(CMakePackage):
    """HyPhy: Hypothesis testing using Phylogenies"""

    homepage = "http://www.hyphy.org/"
    url      = "https://github.com/veg/hyphy/archive/2.3.14.tar.gz"

    version('2.3.14', sha256='9e6c817cb649986e3fe944bcaf88be3533e7e62968b9a486c719e951e5ed1cf6')

    depends_on('cmake@3.0:', type='build')
    depends_on('curl')

    conflicts('%gcc@:4.8')
