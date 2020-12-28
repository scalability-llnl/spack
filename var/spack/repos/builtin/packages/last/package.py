# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Last(MakefilePackage):
    """LAST finds similar regions between sequences, and aligns them. It is
       designed for comparing large datasets to each other (e.g. vertebrate
       genomes and/or large numbers of DNA reads)."""

    homepage = "http://last.cbrc.jp/"
    url      = "http://last.cbrc.jp/last-869.zip"

    version('869', sha256='6371a6282bc1bb02a5e5013cc463625f2ce3e7746ff2ea0bdf9fe6b15605a67c')

    def install(self, spec, prefix):
        make('install', 'prefix=%s' % prefix)
