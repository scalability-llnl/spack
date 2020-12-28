# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imake(AutotoolsPackage, XorgPackage):
    """The imake build system."""

    homepage = "http://www.snake.net/software/imake-stuff/"
    xorg_mirror_path = "util/imake-1.0.7.tar.gz"

    version('1.0.7', sha256='6bda266a07eb33445d513f1e3c82a61e4822ccb94d420643d58e1be5f881e5cb')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
