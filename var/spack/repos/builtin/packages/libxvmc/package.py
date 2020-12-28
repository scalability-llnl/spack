# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxvmc(AutotoolsPackage, XorgPackage):
    """X.org libXvMC library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXvMC"
    xorg_mirror_path = "lib/libXvMC-1.0.9.tar.gz"

    version('1.0.9', sha256='090f087fe65b30b3edfb996c79ff6cf299e473fb25e955fff1c4e9cb624da2c2')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxv')

    depends_on('xextproto', type='build')
    depends_on('videoproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
