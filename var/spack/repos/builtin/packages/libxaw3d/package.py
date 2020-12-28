# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxaw3d(AutotoolsPackage, XorgPackage):
    """Xaw3d is the X 3D Athena Widget Set.
    Xaw3d is a widget set based on the X Toolkit Intrinsics (Xt) Library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXaw3d"
    xorg_mirror_path = "lib/libXaw3d-1.6.2.tar.gz"

    version('1.6.2', sha256='847dab01aeac1448916e3b4edb4425594b3ac2896562d9c7141aa4ac6c898ba9')

    depends_on('libx11')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libxext')
    depends_on('libxpm')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
