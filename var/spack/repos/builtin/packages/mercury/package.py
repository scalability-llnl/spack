# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Mercury(CMakePackage):
    """Mercury is a C library for implementing RPC, optimized for HPC"""

    homepage = 'https://mercury-hpc.github.io/'
    url = 'https://github.com/mercury-hpc/mercury/releases/download/v1.0.1/mercury-1.0.1.tar.bz2'
    git = 'https://github.com/mercury-hpc/mercury.git'

    maintainers = ['soumagne']

    version('master', branch='master', submodules=True)
    version('2.0.0', sha256='9e80923712e25df56014309df70660e828dbeabbe5fcc82ee024bcc86e7eb6b7')
    version('1.0.1', sha256='02febd56c401ef7afa250caf28d012b37dee842bfde7ee16fcd2f741b9cf25b3')
    version('1.0.0', sha256='fb0e44d13f4652f53e21040435f91d452bc2b629b6e98dcf5292cd0bece899d4')
    version('0.9.0', sha256='40868e141cac035213fe79400f8926823fb1f5a0651fd7027cbe162b063843ef')

    variant('bmi', default=False, description='Use BMI plugin')
    variant('cci', default=False, description='Use CCI plugin')
    variant('mpi', default=False, description='Use MPI plugin')
    variant('ofi', default=True,  description='Use OFI libfabric plugin')
    # NOTE: the sm plugin does not require any package dependency.
    variant('sm',  default=True,  description='Use shared-memory plugin')
    # NOTE: if boostsys is False, mercury will install its own copy
    # of the preprocessor headers.
    variant('boostsys', default=True,
            description='Use preprocessor headers from boost dependency')
    variant('shared',   default=True,
            description='Build with shared libraries')
    # NOTE: the 'udreg' variant requires that the MPICH_GNI_NDREG_ENTRIES=1024
    #   environment variable be set at run time to avoid conflicts with
    #   Cray-MPICH if libfabric and MPI are used at the same time
    variant('udreg', default=False,
            description='Enable udreg on supported Cray platforms')
    variant('debug', default=False,
            description='Enable Mercury to print debug output')

    depends_on('cmake@2.8.12.2:', type='build')
    # depends_on('cci', when='+cci')  # TODO: add CCI package
    depends_on('bmi', when='+bmi')
    depends_on('mpi', when='+mpi')
    depends_on('libfabric@1.5:', when='+ofi')
    depends_on('openpa@1.0.3:', when='%gcc@:4.8')
    depends_on('boost@1.48:', when='+boostsys')
    depends_on('boost', when='@:0.9')  # internal boost headers were added in 1.0.0

    conflicts('+ofi', when='@:0.9')    # libfabric support was added in 1.0.0
    conflicts('~ofi', when='+udreg')   # udreg option is specific to OFI

    # Fix CMake check_symbol_exists
    # See https://github.com/mercury-hpc/mercury/issues/299
    patch('fix-cmake-3.15-check_symbol_exists.patch', when='@1.0.0:1.0.1')

    def cmake_args(self):
        """Populate cmake arguments for Mercury."""
        spec = self.spec
        variant_bool = lambda feature: str(feature in spec)
        parallel_tests = '+mpi' in spec and self.run_tests

        cmake_args = [
            '-DBUILD_SHARED_LIBS:BOOL=%s' % variant_bool('+shared'),
            '-DBUILD_TESTING:BOOL=%s' % str(self.run_tests),
            '-DMERCURY_ENABLE_PARALLEL_TESTING:BOOL=%s' % str(parallel_tests),
            '-DMERCURY_USE_BOOST_PP:BOOL=ON',
            '-DMERCURY_USE_CHECKSUMS:BOOL=ON',
            '-DMERCURY_USE_SYSTEM_MCHECKSUM:BOOL=OFF',
            '-DMERCURY_USE_XDR:BOOL=OFF',
            '-DNA_USE_BMI:BOOL=%s' % variant_bool('+bmi'),
            '-DNA_USE_CCI:BOOL=%s' % variant_bool('+cci'),
            '-DNA_USE_MPI:BOOL=%s' % variant_bool('+mpi'),
            '-DNA_USE_SM:BOOL=%s'  % variant_bool('+sm'),
        ]

        if '@2.0.0:' in spec:
            cmake_args.extend([
                '-DMERCURY_ENABLE_DEBUG:BOOL=%s' % variant_bool('+debug'),
            ])

        # Previous versions of mercury had more extensive CMake options
        if '@:1.0.1' in spec:
            cmake_args.extend([
                '-DMERCURY_ENABLE_POST_LIMIT:BOOL=OFF',
                '-DMERCURY_ENABLE_VERBOSE_ERROR=%s' % variant_bool('+debug'),
                '-DMERCURY_USE_EAGER_BULK:BOOL=ON',
                '-DMERCURY_USE_SELF_FORWARD:BOOL=ON',
            ])

        if '@1.0.0:' in spec:
            cmake_args.extend([
                '-DMERCURY_USE_SYSTEM_BOOST:BOOL=%s'
                % variant_bool('+boostsys'),
                '-DNA_USE_OFI:BOOL=%s' % variant_bool('+ofi'),
            ])

        if '+ofi' in spec:
            cmake_args.append(
                '-DNA_OFI_GNI_USE_UDREG:BOOL=%s' % variant_bool('+udreg')
            )
            if self.run_tests:
                cmake_args.append(
                    '-DNA_OFI_TESTING_PROTOCOL:STRING={0}'.format(
                        ';'.join(spec['libfabric'].variants['fabrics'].value)
                    )
                )

        return cmake_args

    def check(self):
        """Unit tests fail when run in parallel."""

        with working_dir(self.build_directory):
            make('test', parallel=False)
