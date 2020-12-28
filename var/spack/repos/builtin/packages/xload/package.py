# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xload(AutotoolsPackage, XorgPackage):
    """xload displays a periodically updating histogram of the
    system load average."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xload"
    xorg_mirror_path = "app/xload-1.1.2.tar.gz"

    version('1.1.2', sha256='4863ad339d22c41a0ca030dc5886404f5ae8b8c47cd5e09f0e36407edbdbe769')

    depends_on('libxaw')
    depends_on('libxmu')
    depends_on('libxt')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
