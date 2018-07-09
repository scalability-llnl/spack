#############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class NetlibLapack(CMakePackage):
    """LAPACK version 3.X is a comprehensive FORTRAN library that does
    linear algebra operations including matrix inversions, least squared
    solutions to linear sets of equations, eigenvector analysis, singular
    value decomposition, etc. It is a very comprehensive and reputable
    package that has found extensive use in the scientific community.

    """
    homepage = "http://www.netlib.org/lapack/"
    url = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.8.0', '96591affdbf58c450d45c1daa540dbd2',
            url='http://www.netlib.org/lapack/lapack-3.8.0.tar.gz')
    version('3.7.1', 'dcdeeed73de152c4643ccc5b1aeb453c')
    version('3.7.0', '697bb8d67c7d336a0f339cc9dd0fa72f')
    version('3.6.1', '421b2cb72e15f237e144428f9c460ee0')
    version('3.6.0', 'f2f6c67134e851fe189bb3ca1fbb5101')
    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')
    version('3.4.2', '61bf1a8a4469d4bdb7604f5897179478')
    version('3.4.1', '44c3869c38c8335c2b9c2a8bb276eb55')
    version('3.4.0', '02d5706ec03ba885fc246e5fa10d8c70')
    version('3.3.1', 'd0d533ec9a5b74933c2a1e84eedc58b4')

    variant('shared', default=True, description="Build shared library version")
    variant('external-blas', default=False,
            description='Build lapack with an external blas')

    variant('lapacke', default=True,
            description='Activates the build of the LAPACKE C interface')
    variant('xblas', default=False,
            description='Builds extended precision routines using XBLAS')

    patch('ibm-xl.patch', when='@3.7: %xl')
    patch('ibm-xl.patch', when='@3.7: %xl_r')

    # virtual dependency
    provides('blas', when='~external-blas')
    provides('lapack')

    depends_on('blas', when='+external-blas')
    depends_on('netlib-xblas+fortran+plain_blas', when='+xblas')
    depends_on('python@2.7:', type='test')

    # We need to run every phase twice in order to get static and shared
    # versions of the libraries. When ~shared, we run the default
    # implementations of the CMakePackage's phases and get only one building
    # directory 'spack-build-static' with -DBUILD_SHARED_LIBS:BOOL=OFF (see
    # implementations of self.build_directory and self.cmake_args() below).
    # When +shared, we run the overridden methods for the phases, each
    # running the default implementation twice with different values for
    # self._building_shared. As a result, we get two building directories:
    # 'spack-build-static' with -DBUILD_SHARED_LIBS:BOOL=OFF and
    # 'spack-build-shared' with -DBUILD_SHARED_LIBS:BOOL=ON.
    _building_shared = False

    def patch(self):
        # Fix cblas CMakeLists.txt -- has wrong case for subdirectory name.
        if self.spec.satisfies('@3.6.0:'):
            filter_file(
                '${CMAKE_CURRENT_SOURCE_DIR}/CMAKE/',
                '${CMAKE_CURRENT_SOURCE_DIR}/cmake/',
                'CBLAS/CMakeLists.txt', string=True)

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): ['libblas'],
            ('c', 'fortran'): [
                'libcblas',
                'libblas',
            ],
            ('c',): [
                'libcblas',
            ],
            ('fortran',): [
                'libblas',
            ]
        }
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]
        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    @property
    def lapack_libs(self):
        shared = True if '+shared' in self.spec else False
        query_parameters = self.spec.last_query.extra_parameters
        query2libraries = {
            tuple(): ['liblapack'],
            ('c', 'fortran'): [
                'liblapacke',
                'liblapack',
            ],
            ('c',): [
                'liblapacke',
            ],
            ('fortran',): [
                'liblapack',
            ]
        }
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]
        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    @property
    def headers(self):
        include_dir = self.spec.prefix.include
        cblas_h = join_path(include_dir, 'cblas.h')
        lapacke_h = join_path(include_dir, 'lapacke.h')
        return HeaderList([cblas_h, lapacke_h])

    @property
    def build_directory(self):
        return join_path(self.stage.source_path,
                         'spack-build-shared' if self._building_shared
                         else 'spack-build-static')

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % (
                'ON' if self._building_shared else 'OFF'),
            '-DLAPACKE:BOOL=%s' % (
                'ON' if '+lapacke' in self.spec else 'OFF'),
            '-DLAPACKE_WITH_TMG:BOOL=%s' % (
                'ON' if '+lapacke' in self.spec else 'OFF')]

        if self.spec.satisfies('@3.6.0:'):
            args.extend(['-DCBLAS=ON'])  # always build CBLAS

        if self.spec.satisfies('%intel'):
            # Intel compiler finds serious syntax issues when trying to
            # build CBLAS and LapackE
            args.extend(['-DCBLAS=OFF'])
            args.extend(['-DLAPACKE:BOOL=OFF'])

        if self.spec.satisfies('%xl') or self.spec.satisfies('%xl_r'):
            # use F77 compiler if IBM XL
            args.extend([
                '-DCMAKE_Fortran_COMPILER=%s' % self.compiler.f77,
                '-DCMAKE_Fortran_FLAGS=%s' % (
                    ' '.join(self.spec.compiler_flags['fflags'])),
            ])

        # deprecated routines are commonly needed by, for example, suitesparse
        # Note that OpenBLAS spack is built with deprecated routines
        args.extend(['-DBUILD_DEPRECATED:BOOL=ON'])

        if '+external-blas' in self.spec:
            args.extend([
                '-DUSE_OPTIMIZED_BLAS:BOOL=ON',
                '-DBLAS_LIBRARIES:PATH=%s' % self.spec['blas'].libs.joined(';')
            ])

        if self.spec.satisfies('+xblas'):
            xblas_include_dir = self.spec['netlib-xblas'].prefix.include
            xblas_library = self.spec['netlib-xblas'].libs.joined(';')
            args.extend([
                '-DXBLAS_INCLUDE_DIR={0}'.format(xblas_include_dir),
                '-DXBLAS_LIBRARY={0}'.format(xblas_library)])

        args.append('-DBUILD_TESTING:BOOL=%s' %
                    ('ON' if self.run_tests else 'OFF'))

        return args

    # Build, install, and check both static and shared versions of the
    # libraries when +shared
    @when('+shared')
    def cmake(self, spec, prefix):
        for self._building_shared in range(2):
            super(NetlibLapack, self).cmake(spec, prefix)

    @when('+shared')
    def build(self, spec, prefix):
        for self._building_shared in range(2):
            super(NetlibLapack, self).build(spec, prefix)

    @when('+shared')
    def install(self, spec, prefix):
        for self._building_shared in range(2):
            super(NetlibLapack, self).install(spec, prefix)

    @when('+shared')
    def check(self):
        for self._building_shared in range(2):
            super(NetlibLapack, self).check()
