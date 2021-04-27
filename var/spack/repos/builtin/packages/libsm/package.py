# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsm(AutotoolsPackage, XorgPackage):
    """libSM - X Session Management Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libSM"
    xorg_mirror_path = "lib/libSM-1.2.2.tar.gz"

    version('1.2.3', sha256='1e92408417cb6c6c477a8a6104291001a40b3bb56a4a60608fdd9cd2c5a0f320')
    version('1.2.2', sha256='14bb7c669ce2b8ff712fbdbf48120e3742a77edcd5e025d6b3325ed30cf120f4')

    depends_on('libice@1.0.5:')
    depends_on('uuid')

    depends_on('xproto')
    depends_on('xtrans')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries('libSM', self.prefix,
                              shared=True, recursive=True)
