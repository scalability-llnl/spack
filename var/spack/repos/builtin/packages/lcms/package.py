# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lcms(AutotoolsPackage):
    """Little cms is a color management library. Implements fast
       transforms between ICC profiles. It is focused on speed, and is
       portable across several platforms (MIT license)."""

    homepage = "http://www.littlecms.com"
    url      = "http://downloads.sourceforge.net/project/lcms/lcms/2.9/lcms2-2.9.tar.gz"

    version('2.9', sha256='48c6fdf98396fa245ed86e622028caf49b96fa22f3e5734f853f806fbc8e7d20')
    version('2.8', sha256='66d02b229d2ea9474e62c2b6cd6720fde946155cd1d0d2bffdab829790a0fb22')
    version('2.6', sha256='5172528839647c54c3da211837225e221be93e4733f5b5e9f57668f7107e14b1')

    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('zlib')

    @property
    def libs(self):
        return find_libraries('liblcms2', root=self.prefix, recursive=True)
