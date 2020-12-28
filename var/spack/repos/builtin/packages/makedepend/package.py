# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Makedepend(AutotoolsPackage, XorgPackage):
    """makedepend - create dependencies in makefiles."""

    homepage = "http://cgit.freedesktop.org/xorg/util/makedepend"
    xorg_mirror_path = "util/makedepend-1.0.5.tar.gz"

    version('1.0.5', sha256='503903d41fb5badb73cb70d7b3740c8b30fe1cc68c504d3b6a85e6644c4e5004')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
