# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Coinutils(AutotoolsPackage):
    """CoinUtils is an open-source collection of classes and helper
    functions that are generally useful to multiple COIN-OR
    projects."""

    homepage = "https://projects.coin-or.org/Coinutils"
    url      = "https://github.com/coin-or/CoinUtils/archive/releases/2.11.4.tar.gz"

    version('2.11.4', sha256='d4effff4452e73356eed9f889efd9c44fe9cd68bd37b608a5ebb2c58bd45ef81')

    build_directory = 'spack-build'
