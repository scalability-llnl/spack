# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwininfo(AutotoolsPackage, XorgPackage):
    """xwininfo prints information about windows on an X server. Various
    information is displayed depending on which options are selected."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xwininfo"
    xorg_mirror_path = "app/xwininfo-1.1.3.tar.gz"

    version('1.1.3', sha256='784f8b9c9ddab24ce4faa65fde6430a8d7cf3c0564573582452cc99c599bd941')

    depends_on('libxcb@1.6:')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
