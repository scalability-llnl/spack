# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xlsclients(AutotoolsPackage, XorgPackage):
    """xlsclients is a utility for listing information about the client
    applications running on a X11 server."""

    homepage = "http://cgit.freedesktop.org/xorg/app/xlsclients"
    xorg_mirror_path = "app/xlsclients-1.1.3.tar.gz"

    version('1.1.3', sha256='4670a4003aae01e9172efb969246c3d8f33481f290aa8726ff50398c838e6994')

    depends_on('libxcb@1.6:', when='@1.1:')
    depends_on('libx11', when='@:1.0')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
