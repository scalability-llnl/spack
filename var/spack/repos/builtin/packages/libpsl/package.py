# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpsl(AutotoolsPackage):
    """libpsl - C library to handle the Public Suffix List."""

    homepage = "https://github.com/rockdaboot/libpsl"
    url      = "https://github.com/rockdaboot/libpsl/releases/download/libpsl-0.17.0/libpsl-0.17.0.tar.gz"

    version('0.17.0', sha256='025729d6a26ffd53cb54b4d86196f62c01d1813a4360c627546c6eb60ce3dd4b')

    depends_on('icu4c')

    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7:', type='build')

    depends_on('valgrind~mpi~boost', type='test')

    def configure_args(self):
        spec = self.spec

        args = [
            'PYTHON={0}'.format(spec['python'].command.path),
        ]

        if self.run_tests:
            args.append('--enable-valgrind-tests')
        else:
            args.append('--disable-valgrind-tests')

        return args
