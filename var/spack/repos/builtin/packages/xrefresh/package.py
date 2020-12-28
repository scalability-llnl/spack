# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xrefresh(AutotoolsPackage, XorgPackage):
    """xrefresh - refresh all or part of an X screen."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xrefresh"
    xorg_mirror_path = "app/xrefresh-1.0.5.tar.gz"

    version('1.0.5', sha256='b373cc1ecd37c3d787e7074ce89a8a06ea173d7ba9e73fa48de973c759fbcf38')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
