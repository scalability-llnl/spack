# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xsm(AutotoolsPackage, XorgPackage):
    """X Session Manager."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xsm"
    xorg_mirror_path = "app/xsm-1.0.3.tar.gz"

    version('1.0.3', sha256='f70815139d62416dbec5915ec37db66f325932a69f6350bb1a74c0940cdc796a')

    depends_on('libx11')
    depends_on('libxt@1.1.0:')
    depends_on('libice')
    depends_on('libsm')
    depends_on('libxaw')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
