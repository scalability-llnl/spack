# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.build_systems.cmake import CMakePackage


class Essl(Package):
    """IBM's Engineering and Scientific Subroutine Library (ESSL)."""

    homepage = "https://www.ibm.com/systems/power/software/essl/"

    variant('ilp64', default=False, description='64 bit integers')
    variant(
        'threads', default='openmp',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )
    variant('cuda', default=False, description='CUDA acceleration')

    provides('blas')

    conflicts('+cuda', when='+ilp64',
              msg='ESSL+cuda+ilp64 cannot combine CUDA acceleration'
              ' 64 bit integers')

    conflicts('+cuda', when='threads=none',
              msg='ESSL+cuda threads=none cannot combine CUDA acceleration'
              ' without multithreading support')

    @property
    def blas_libs(self):
        spec = self.spec
        prefix = self.prefix

        if '+ilp64' in spec:
            essl_lib = ['libessl6464']
        else:
            essl_lib = ['libessl']

        if spec.satisfies('threads=openmp'):
            # ESSL SMP support requires XL or Clang OpenMP library
            if '%xl' in spec or '%xl_r' in spec or '%clang' in spec:
                if '+ilp64' in spec:
                    essl_lib = ['libesslsmp6464']
                else:
                    if '+cuda' in spec:
                        essl_lib = ['libesslsmpcuda']
                    else:
                        essl_lib = ['libesslsmp']

        essl_root = prefix.lib64
        essl_libs = find_libraries(
            essl_lib,
            root=essl_root,
            shared=True
        )

        return essl_libs

    @property
    def blas_cmake_args(self):
        return [
            CMakePackage.define('BLA_STATIC', False),
            CMakePackage.define('BLA_VENDOR', 'IBMESSL'),
        ]

    def install(self, spec, prefix):
        raise InstallError('IBM ESSL is not installable;'
                           ' it is vendor supplied')
