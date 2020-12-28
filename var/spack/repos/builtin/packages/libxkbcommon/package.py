# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxkbcommon(AutotoolsPackage):
    """xkbcommon is a library to handle keyboard descriptions, including
    loading them from disk, parsing them and handling their state. It's mainly
    meant for client toolkits, window systems, and other system
    applications."""

    homepage = "https://xkbcommon.org/"
    url      = "https://xkbcommon.org/download/libxkbcommon-0.8.2.tar.xz"

    version('0.8.2', sha256='7ab8c4b3403d89d01898066b72cb6069bddeb5af94905a65368f671a026ed58c')
    version('0.8.0', sha256='e829265db04e0aebfb0591b6dc3377b64599558167846c3f5ee5c5e53641fe6d')
    version('0.7.1', sha256='ba59305d2e19e47c27ea065c2e0df96ebac6a3c6e97e28ae5620073b6084e68b')

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('bison', type='build')
    depends_on('util-macros')
    depends_on('xkbdata')
    depends_on('libxcb@1.10:')

    def configure_args(self):
        return [
            '--with-xkb-config-root={0}'.format(self.spec['xkbdata'].prefix)
        ]
