# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librsb(AutotoolsPackage):
    """librsb : A shared memory parallel sparse matrix computations
    library for the Recursive Sparse Blocks format"""

    homepage = "http://librsb.sourceforge.net/"
    url      = "http://download.sourceforge.net/librsb/librsb-1.2.0.9.tar.gz"
    list_url = "https://sourceforge.net/projects/librsb/files/"

    version('1.2.0.9',   'f421f5d572461601120933e3c1cfee2ca69e6ecc92cbb11baa4e86bdedd3d9fa')
    version('1.2.0.8',   '8bebd19a1866d80ade13eabfdd0f07ae7e8a485c0b975b5d15f531ac204d80cb')

    depends_on('zlib')
    conflicts('%apple-clang')
    conflicts('%clang')

    def configure_args(self):
        args = [
            '--enable-openmp',
            '--with-zlib',
            '--enable-fortran-module-install',
            'CPPFLAGS={0}'.format(self.spec['zlib'].headers.include_flags),
            'CFLAGS=-O3',
            'LDFLAGS={0}'.format(self.spec['zlib'].libs.search_flags)
        ]
        return args
