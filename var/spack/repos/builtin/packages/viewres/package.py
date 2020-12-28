# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Viewres(AutotoolsPackage, XorgPackage):
    """viewres displays a tree showing the widget class hierarchy of the
    Athena Widget Set (libXaw)."""

    homepage = "http://cgit.freedesktop.org/xorg/app/viewres"
    xorg_mirror_path = "app/viewres-1.0.4.tar.gz"

    version('1.0.4', sha256='fd2aaec85c952fd6984fe14d0fcbda4d2ab9849a9183e4787b0ef552a10a87a1')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
