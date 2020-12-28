# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Giflib(AutotoolsPackage, SourceforgePackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "http://giflib.sourceforge.net/"
    sourceforge_mirror_path = "giflib/giflib-5.1.4.tar.bz2"

    version('5.1.4', sha256='df27ec3ff24671f80b29e6ab1c4971059c14ac3db95406884fc26574631ba8d5')

    patch('bsd-head.patch')

    def check(self):
        make('check', parallel=False)
