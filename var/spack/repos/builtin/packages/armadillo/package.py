# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Armadillo(CMakePackage):
    """Armadillo is a high quality linear algebra library (matrix maths)
    for the C++ language, aiming towards a good balance between speed and
    ease of use."""

    homepage = "http://arma.sourceforge.net/"
    url = "http://sourceforge.net/projects/arma/files/armadillo-8.100.1.tar.xz"

    version('9.800.3', sha256='a481e1dc880b7cb352f8a28b67fe005dc1117d4341277f12999a2355d40d7599')
    version('8.100.1', sha256='54773f7d828bd3885c598f90122b530ded65d9b195c9034e082baea737cd138d')
    version('7.950.1', sha256='a32da32a0ea420b8397a53e4b40ed279c1a5fc791dd492a2ced81ffb14ad0d1b')

    variant('hdf5', default=False, description='Include HDF5 support')

    depends_on('cmake@2.8.12:', type='build')
    depends_on('arpack-ng')  # old arpack causes undefined symbols
    depends_on('blas')
    depends_on('lapack')
    depends_on('superlu@5.2:')
    depends_on('hdf5', when='+hdf5')

    # Adds an `#undef linux` to prevent preprocessor expansion of include
    # directories with `linux` in them getting transformed into a 1.
    # E.g. `/path/linux-x86_64/dir` -> `/path/1-x86_64/dir` if/when a linux
    # platform's compiler is adding `#define linux 1`.
    patch('undef_linux.patch', when='platform=linux')

    def cmake_args(self):
        spec = self.spec

        return [
            # ARPACK support
            '-DARPACK_LIBRARY={0}'.format(spec['arpack-ng'].libs.joined(";")),
            # BLAS support
            '-DBLAS_LIBRARY={0}'.format(spec['blas'].libs.joined(";")),
            # LAPACK support
            '-DLAPACK_LIBRARY={0}'.format(spec['lapack'].libs.joined(";")),
            # SuperLU support
            '-DSuperLU_INCLUDE_DIR={0}'.format(spec['superlu'].prefix.include),
            '-DSuperLU_LIBRARY={0}'.format(spec['superlu'].libs.joined(";")),
            # HDF5 support
            '-DDETECT_HDF5={0}'.format('ON' if '+hdf5' in spec else 'OFF')
        ]
