# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class StadenIoLib(AutotoolsPackage):
    """Io_lib is a library for reading/writing various bioinformatics
       file formats."""

    homepage = "http://staden.sourceforge.net/"
    url      = "https://sourceforge.net/projects/staden/files/io_lib/1.14.8/io_lib-1.14.8.tar.gz/download"

    version('1.14.8', sha256='3bd560309fd6d70b14bbb8230e1baf8706b804eb6201220bb6c3d6db72003d1b')

    variant('curl', default=False, description='Build with curl support')

    depends_on('zlib')
    depends_on('curl', when='+curl')

    def configure_args(self):
        args = []

        if self.spec.satisfies('~curl'):
            args.append('--without-libcurl')

        return args
