# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Mixedversions(Package):
    url = "http://www.fake-mixedversions.org/downloads/mixedversions-1.0.tar.gz"

    version('2.0.1', 'hashc')
    version('2.0', 'hashb')
    version('1.0.1', 'hasha')
