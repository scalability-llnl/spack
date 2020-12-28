# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zziplib(AutotoolsPackage):
    """The zziplib provides read access to zipped files in a zip-archive, using
    compression based solely on free algorithms provided by zlib.  It also
    provides a functionality to overlay the archive filesystem with the
    filesystem of the operating system environment."""

    homepage = "https://github.com/gdraheim/zziplib"
    url      = "https://github.com/gdraheim/zziplib/archive/v0.13.69.tar.gz"

    version('0.13.69', sha256='846246d7cdeee405d8d21e2922c6e97f55f24ecbe3b6dcf5778073a88f120544')

    patch('python2to3.patch')

    build_directory = 'spack-build'

    depends_on('python', type='build')
    depends_on('zlib')

    def configure_args(self):
        args = ['--with-zlib={0}'.format(self.spec['zlib'].prefix)]
        return args
