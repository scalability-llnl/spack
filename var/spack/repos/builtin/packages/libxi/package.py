# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxi(AutotoolsPackage, XorgPackage):
    """libXi - library for the X Input Extension."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXi"
    xorg_mirror_path = "lib/libXi-1.7.6.tar.gz"

    version('1.7.6', sha256='4e88fa7decd287e58140ea72238f8d54e4791de302938c83695fc0c9ac102b7e')

    depends_on('pkgconfig', type='build')
    depends_on('libx11@1.6:')
    depends_on('libxext@1.0.99.1:')
    depends_on('libxfixes@5:')

    # transient build dependency (from libxfixes), i.e. shouldn't be needed?
    depends_on('fixesproto@5.0:', type='build')

    depends_on('xproto@7.0.13:', type='build')
    depends_on('xextproto@7.0.3:', type='build')
    depends_on('inputproto@2.2.99.1:', type='build')

    @property
    def libs(self):
        return find_libraries(
            'libXi', self.prefix, shared=True, recursive=True)
