# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libice(AutotoolsPackage, XorgPackage):
    """libICE - Inter-Client Exchange Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libICE"
    xorg_mirror_path = "lib/libICE-1.0.9.tar.gz"

    version('1.0.9', sha256='7812a824a66dd654c830d21982749b3b563d9c2dfe0b88b203cefc14a891edc0')

    depends_on('xproto')
    depends_on('xtrans')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    @property
    def libs(self):
        return find_libraries('libICE', self.prefix,
                              shared=True, recursive=True)
