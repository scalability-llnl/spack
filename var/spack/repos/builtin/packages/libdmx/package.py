# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdmx(AutotoolsPackage, XorgPackage):
    """libdmx - X Window System DMX (Distributed Multihead X) extension
    library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libdmx"
    xorg_mirror_path = "lib/libdmx-1.1.3.tar.gz"

    version('1.1.3', sha256='c4b24d7e13e5a67ead7a18f0b4cc9b7b5363c9d04cd01b83b5122ff92b3b4996')

    depends_on('libx11')
    depends_on('libxext')

    depends_on('xextproto', type='build')
    depends_on('dmxproto@2.2.99.1:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
