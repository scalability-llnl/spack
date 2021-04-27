# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Imake(AutotoolsPackage, XorgPackage):
    """The imake build system."""

    homepage = "http://www.snake.net/software/imake-stuff/"
    xorg_mirror_path = "util/imake-1.0.7.tar.gz"

    version('1.0.7', sha256='6bda266a07eb33445d513f1e3c82a61e4822ccb94d420643d58e1be5f881e5cb')

    depends_on('xproto')
    depends_on('xorg-cf-files', type='run')
    depends_on('pkgconfig', type='build')

    def configure_args(self):
        args = []
        cfgdir = self.spec['xorg-cf-files'].prefix.lib.X11.config
        args.append('--with-config-dir={0}'.format(cfgdir))
        return args
