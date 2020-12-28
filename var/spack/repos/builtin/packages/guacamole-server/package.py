# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GuacamoleServer(AutotoolsPackage):
    """The guacamole-server package is a set of software which forms the
    basis of the Guacamole stack. It consists of guacd, libguac, and
    several protocol support libraries."""

    homepage = "http://guacamole.apache.org/"
    url      = "https://github.com/apache/guacamole-server/archive/1.1.0.tar.gz"

    version('1.1.0',     sha256='d0f0c66ebfa7a4fd6689ae5240f21797b5177945a042388b691b15b8bd5c81a8')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('cairo')
    depends_on('libjpeg')
    depends_on('libpng')
    depends_on('uuid')
