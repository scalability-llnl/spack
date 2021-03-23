# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Haveged(AutotoolsPackage):
    """A Linux entropy source using the HAVEGE algorithm."""

    homepage = "https://github.com/jirka-h/haveged"
    url      = "https://github.com/jirka-h/haveged/archive/v1.9.13/haveged-1.9.13.tar.gz"

    version('1.9.13', sha256='d17bd22fa1745daca5ac72e014ed3b0fe5720da4c115953124b1bf2a0aa2b04b')
