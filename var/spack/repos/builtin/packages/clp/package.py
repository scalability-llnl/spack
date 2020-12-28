# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clp(AutotoolsPackage):
    """Clp (Coin-or linear programming) is an open-source
      linear programming solver written in C++."""

    homepage = "https://projects.coin-or.org/Clp"
    url      = "https://github.com/coin-or/Clp/archive/releases/1.17.6.tar.gz"

    depends_on('coinutils')
    depends_on('osi')

    version('1.17.6', sha256='afff465b1620cfcbb7b7c17b5d331d412039650ff471c4160c7eb24ae01284c9')
    version('1.17.4', sha256='ef412cde00cb1313d9041115a700d8d59d4b8b8b5e4dde43e9deb5108fcfbea8')
    version('1.16.11', sha256='b525451423a9a09a043e6a13d9436e13e3ee7a7049f558ad41a110742fa65f39')

    build_directory = 'spack-build'
