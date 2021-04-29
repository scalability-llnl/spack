# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Apex(CMakePackage):
    """Autonomic Performance Environment for eXascale (APEX)."""

    maintainers = ['khuck']
    homepage = "https://github.com/khuck/xpress-apex"
    url      = "https://github.com/khuck/xpress-apex/archive/v2.2.0.tar.gz"
    git      = "https://github.com/khuck/xpress-apex"

    version('develop', branch='develop')
    version('master', branch='master')
    version('2.3.1', sha256='86bf6933f2c53531fcb24cda9fc7dc9919909bed54740d1e0bc3e7ce6ed78091')
    version('2.3.0', sha256='7e1d16c9651b913c5e28abdbad75f25c55ba25e9fa35f5d979c1d3f9b9852c58')
    version('2.2.0', sha256='cd5eddb1f6d26b7dbb4a8afeca2aa28036c7d0987e0af0400f4f96733889c75c')

    # Disable some default dependencies on Darwin/OSX
    darwin_default = False
    if sys.platform != 'darwin':
        darwin_default = True

    # Enable by default
    variant('activeharmony', default=True, description='Enables Active Harmony support')
    variant('plugins', default=True, description='Enables Policy Plugin support')
    variant('binutils', default=True, description='Enables Binutils support')
    variant('otf2', default=True, description='Enables OTF2 support')
    variant('gperftools', default=True, description='Enables Google PerfTools TCMalloc support')
    variant('openmp', default=darwin_default, description='Enables OpenMP support')
    variant('papi', default=darwin_default, description='Enables PAPI support')

    # Disable by default
    variant('cuda', default=False, description='Enables CUDA support')
    variant('boost', default=False, description='Enables Boost support')
    variant('jemalloc', default=False, description='Enables JEMalloc support')
    variant('lmsensors', default=False, description='Enables LM-Sensors support')
    variant('mpi', default=False, description='Enables MPI support')
    variant('tests', default=False, description='Build Unit Tests')
    variant('examples', default=False, description='Build Examples')

    # Dependencies
    depends_on('cmake', type='build')
    depends_on('binutils+libiberty+headers', when='+binutils')
    depends_on('activeharmony@4.6:', when='+activeharmony')
    depends_on('activeharmony@4.6:', when='+plugins')
    depends_on('otf2', when='+otf2')
    depends_on('mpi', when='+mpi')
    depends_on('gperftools', when='+gperftools')
    depends_on('jemalloc', when='+jemalloc')
    depends_on('papi', when='+papi')
    depends_on('cuda', when='+cuda')
    depends_on('boost@1.54:', when='+boost')

    # Conflicts
    conflicts('+jemalloc', when='+gperftools')
    conflicts('+plugins', when='~activeharmony')

    def cmake_args(self):
        args = []
        spec = self.spec
        # CMake variables were updated in version 2.3.0, to make
        prefix = 'APEX_WITH'
        test_prefix = 'APEX_'
        if '@2.2.0' in spec:
            prefix = 'USE'
            test_prefix = ''

        if '+cuda' in spec:
            args.append('-DAPEX_WITH_CUDA=TRUE')
        else:
            args.append('-DAPEX_WITH_CUDA=FALSE')

        if '+binutils' in spec:
            args.append('-DBFD_ROOT={0}'.format(spec['binutils'].prefix))
            args.append('-D' + prefix + '_BFD=TRUE')
        else:
            args.append('-D' + prefix + '_BFD=FALSE')

        if '+activeharmony' in spec:
            args.append('-DACTIVEHARMONY_ROOT={0}'.format(
                spec['activeharmony'].prefix))
            args.append('-D' + prefix + '_ACTIVEHARMONY=TRUE')
        else:
            args.append('-D' + prefix + '_ACTIVEHARMONY=FALSE')

        if '+plugins' in spec:
            args.append('-D' + prefix + '_PLUGINS=TRUE')
        else:
            args.append('-D' + prefix + '_PLUGINS=FALSE')

        if '+lmsensors' in spec:
            args.append('-D' + prefix + '_LM_SENSORS=TRUE')
        else:
            args.append('-D' + prefix + '_LM_SENSORS=FALSE')

        if '+mpi' in spec:
            args.append('-D' + prefix + '_MPI=TRUE')
        else:
            args.append('-D' + prefix + '_MPI=FALSE')

        if '+otf2' in spec:
            args.append('-DOTF2_ROOT={0}'.format(spec['otf2'].prefix))
            args.append('-D' + prefix + '_OTF2=TRUE')
        else:
            args.append('-D' + prefix + '_OTF2=FALSE')

        if '+openmp' in spec:
            args.append('-D' + prefix + '_OMPT=TRUE')
        else:
            args.append('-D' + prefix + '_OMPT=FALSE')

        if '+gperftools' in spec:
            args.append('-DGPERFTOOLS_ROOT={0}'.format(
                spec['gperftools'].prefix))
            args.append('-D' + prefix + '_TCMALLOC=TRUE')
        else:
            args.append('-D' + prefix + '_TCMALLOC=FALSE')

        if '+jemalloc' in spec:
            args.append('-DJEMALLOC_ROOT={0}'.format(spec['jemalloc'].prefix))
            args.append('-D' + prefix + '_JEMALLOC=TRUE')
        else:
            args.append('-D' + prefix + '_JEMALLOC=FALSE')

        if '+boost' in spec:
            args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))

        if '+tests' in spec:
            args.append('-D' + test_prefix + 'BUILD_TESTS=TRUE')
        else:
            args.append('-D' + test_prefix + 'BUILD_TESTS=FALSE')

        if '+examples' in spec:
            args.append('-D' + test_prefix + 'BUILD_EXAMPLES=TRUE')
        else:
            args.append('-D' + test_prefix + 'BUILD_EXAMPLES=FALSE')

        return args
