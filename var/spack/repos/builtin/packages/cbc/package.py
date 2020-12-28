# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cbc(AutotoolsPackage):
    """Cbc (Coin-or branch and cut) is an open-source mixed integer
    linear programming solver written in C++. It can be used as a
    callable library or using a stand-alone executable."""

    homepage = "https://projects.coin-or.org/Cbc"
    url      = "https://github.com/coin-or/Cbc/archive/releases/2.10.5.tar.gz"

    depends_on('coinutils')
    depends_on('osi')
    depends_on('cgl')

    version('2.10.5', sha256='cc44c1950ff4615e7791d7e03ea34318ca001d3cac6dc3f7f5ee392459ce6719')

    build_directory = 'spack-build'
