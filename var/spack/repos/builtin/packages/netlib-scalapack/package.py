# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class ScalapackBase(CMakePackage):
    """Base class for building ScaLAPACK, shared with the AMD optimized version
    of the library in the 'amdscalapack' package.
    """
    variant(
        'build_type',
        default='Release',
        description='CMake build type',
        values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant(
        'shared',
        default=True,
        description='Build the shared library version'
    )
    variant(
        'pic',
        default=False,
        description='Build position independent code'
    )

    provides('scalapack')

    depends_on('mpi')
    depends_on('lapack')
    depends_on('blas')
    depends_on('cmake', when='@2.0.0:', type='build')

    # See: https://github.com/Reference-ScaLAPACK/scalapack/issues/9
    patch("cmake_fortran_mangle.patch", when='@2.0.2:2.0.99')
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/10
    patch("mpi2-compatibility.patch", when='@2.0.2:2.0.99')
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/16
    patch("int_overflow.patch", when='@2.0.0:2.1.0')
    # See: https://github.com/Reference-ScaLAPACK/scalapack/pull/23
    patch("gcc10-compatibility.patch", when='@2.0.0:2.1.0')

    @property
    def libs(self):
        # Note that the default will be to search
        # for 'libnetlib-scalapack.<suffix>'
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libscalapack', root=self.prefix, shared=shared, recursive=True
        )

    def cmake_args(self):
        spec = self.spec

        options = [
            "-DBUILD_SHARED_LIBS:BOOL=%s" % ('ON' if '+shared' in spec else
                                             'OFF'),
            "-DBUILD_STATIC_LIBS:BOOL=%s" % ('OFF' if '+shared' in spec else
                                             'ON')
        ]

        # Make sure we use Spack's Lapack:
        blas = spec['blas'].libs
        lapack = spec['lapack'].libs
        options.extend([
            '-DLAPACK_FOUND=true',
            '-DLAPACK_INCLUDE_DIRS=%s' % spec['lapack'].prefix.include,
            '-DLAPACK_LIBRARIES=%s' % (lapack.joined(';')),
            '-DBLAS_LIBRARIES=%s' % (blas.joined(';'))
        ])

        if '+pic' in spec:
            options.extend([
                "-DCMAKE_C_FLAGS=%s" % self.compiler.cc_pic_flag,
                "-DCMAKE_Fortran_FLAGS=%s" % self.compiler.fc_pic_flag
            ])

        return options

    @run_after('install')
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if (sys.platform == 'darwin') and ('+shared' in self.spec):
            fix_darwin_install_name(self.spec.prefix.lib)


class NetlibScalapack(ScalapackBase):
    """ScaLAPACK is a library of high-performance linear algebra routines for
    parallel distributed memory machines
    """

    homepage = "http://www.netlib.org/scalapack/"
    url = "http://www.netlib.org/scalapack/scalapack-2.0.2.tgz"

    version('2.1.0', sha256='61d9216cf81d246944720cfce96255878a3f85dec13b9351f1fa0fd6768220a6')
    version('2.0.2', sha256='0c74aeae690fe5ee4db7926f49c5d0bb69ce09eea75beb915e00bba07530395c')
    version('2.0.1', sha256='a9b34278d4e10b40cbe084c6d87d09af8845e874250719bfbbc497b2a88bfde1')
    version('2.0.0', sha256='e51fbd9c3ef3a0dbd81385b868e2355900148eea689bf915c5383d72daf73114')
    # versions before 2.0.0 are not using cmake and requires blacs as
    # a separated package
