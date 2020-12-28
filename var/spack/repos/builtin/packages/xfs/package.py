# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfs(AutotoolsPackage, XorgPackage):
    """X Font Server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xfs"
    xorg_mirror_path = "app/xfs-1.1.4.tar.gz"

    version('1.1.4', sha256='28f89b854d1ff14fa1efa5b408e5e1c4f6a145420310073c4e44705feeb6d23b')

    depends_on('libxfont@1.4.5:')
    depends_on('font-util')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('fontsproto', type='build')
    depends_on('xtrans', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
