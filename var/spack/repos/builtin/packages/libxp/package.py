# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxp(AutotoolsPackage, XorgPackage):
    """libXp - X Print Client Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXp"
    xorg_mirror_path = "lib/libXp-1.0.3.tar.gz"

    version('1.0.3', sha256='f6b8cc4ef05d3eafc9ef5fc72819dd412024b4ed60197c0d5914758125817e9c')

    depends_on('libx11@1.6:')
    depends_on('libxext')
    depends_on('libxau')

    depends_on('xextproto', type='build')
    depends_on('printproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
