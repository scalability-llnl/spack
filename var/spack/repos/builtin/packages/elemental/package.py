##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Elemental(CMakePackage):
    """Elemental: Distributed-memory dense and sparse-direct linear algebra and optimization library."""

    homepage = "http://libelemental.org"
    url      = "https://github.com/elemental/Elemental/archive/v0.87.6.tar.gz"

    version('0.87.6', '9fd29783d45b0a0e27c0df85f548abe9')

    variant('debug', default=False, 
            description='Builds a debug version of the libraries')
    variant('shared', default=True, 
            description='Enables the build of shared libraries')
    variant('hybrid', default=True, 
            description='Make use of OpenMP within MPI packing/unpacking')
    variant('openmp_blas', default=False,
            description='Use OpenMP for threading in the BLAS library')
    variant('c_interface', default=False, 
            description='Build C interface')
    variant('python', default=False, 
            description='Install Python interface')
    variant('parmetis', default=False, 
            description='Enable ParMETIS')
    variant('quad', default=False, 
            description='Enable quad precision')
    variant('int64', default=False, 
            description='Use 64bit integers')
    # When this variant is set remove the normal dependencies since
    # Elemental has to build BLAS and ScaLAPACK internally
    variant('int64_blas', default=False, 
            description='Use 64bit integers for BLAS.' 
            ' Requires local build of BLAS library.')
    variant('scalapack', default=False,
            description='Build with ScaLAPACK library')

    depends_on('cmake', type='build')
    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('blas', when='~openmp_blas ~int64_blas') # Hack until issue #1712 is fixed
    # Hack to forward variant to openblas package
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('openblas +openmp', when='+openmp_blas ~int64_blas')
    # Note that this forces us to use OpenBLAS until #1712 is fixed
    depends_on('lapack', when='~openmp_blas')
    depends_on('metis')
    depends_on('metis +int64', when='+int64')
    depends_on('mpi')
    # Allow Elemental to build internally when using 8-byte ints
    depends_on('scalapack', when='+scalapack ~int64_blas')
    depends_on('python', when='+python')

    def build_type(self):
        """Returns the correct value for the ``CMAKE_BUILD_TYPE`` variable
        :return: value for ``CMAKE_BUILD_TYPE``
        """
        if '+debug' in self.spec:
            return 'Debug'
        else:
            return 'Release'

    def cmake_args(self):
        args = ['-DCMAKE_INSTALL_MESSAGE:STRING=LAZY',
                '-DEL_PREFER_OPENBLAS:BOOL=TRUE',
                '-DEL_DISABLE_SCALAPACK:BOOL={0}'.format((
                    'OFF' if '+scalapack' in self.spec else 'ON')),
                '-DGFORTRAN_LIB=libgfortran.so',
                '-DBUILD_SHARED_LIBS:BOOL={0}'.format((
                    'ON' if '+shared' in self.spec else 'OFF')),
                '-DEL_HYBRID:BOOL={0}'.format((
                    'ON' if '+hybrid' in self.spec else 'OFF')),
                '-DEL_C_INTERFACE:BOOL={0}'.format((
                    'ON' if '+c_interface' in self.spec else 'OFF')),
                '-DINSTALL_PYTHON_PACKAGE:BOOL={0}'.format((
                    'ON' if '+python' in self.spec else 'OFF')),
                '-DEL_DISABLE_PARMETIS:BOOL={0}'.format((
                    'OFF' if '+parmetis' in self.spec else 'ON')),
                '-DEL_DISABLE_QUAD:BOOL={0}'.format((
                    'OFF' if '+quad' in self.spec else 'ON')),
                '-DEL_USE_64BIT_INTS:BOOL={0}'.format((
                    'ON' if '+int64' in self.spec else 'OFF')),
                '-DEL_USE_64BIT_BLAS_INTS:BOOL={0}'.format((
                    'ON' if '+int64_blas' in self.spec else 'OFF'))]
        if '+int64_blas' in self.spec:
            args.extend(['-DEL_BLAS_SUFFIX:STRING={0}'.format((
                '_64_' if '+int64_blas' in self.spec else '_')),
                         '-DCUSTOM_BLAS_SUFFIX:BOOL=TRUE']),
            if '+scalapack' in self.spec:
                args.extend(['-DEL_LAPACK_SUFFIX:STRING={0}'.format((
                    '_64_' if '+int64_blas' in self.spec else '_')),
                             '-DCUSTOM_LAPACK_SUFFIX:BOOL=TRUE']),
        else:
            lapack = self.spec['lapack'].lapack_libs
            blas = self.spec['blas'].blas_libs

            if '+scalapack' in self.spec:
                scalapack = self.spec['scalapack'].scalapack_libs
                args.extend(['-DMATH_LIBS:STRING={0} {1}'.format(
                    (lapack + blas).search_flags, scalapack.search_flags),
                             '-DMATH_LIBS:STRING={0} {1}'.format(
                    (lapack + blas).ld_flags.split()[1], scalapack.ld_flags.split()[1])])
            else:
                args.extend(['-DMATH_LIBS:STRING={0}'.format(
                    (lapack + blas).search_flags),
                             '-DMATH_LIBS:STRING={0}'.format(
                    (lapack + blas).ld_flags.split()[1])])
        return args
