# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack.package import *


class Timemory(CMakePackage):
    """Timing + Memory + Hardware Counter Utilities for C/C++/CUDA/Python"""

    homepage = 'https://timemory.readthedocs.io/en/latest/'
    git = 'https://github.com/NERSC/timemory.git'
    maintainers = ['jrmadsen']

    version('master', branch='master', submodules=True)
    version('develop', branch='develop', submodules=True)
    version('3.0.1', commit='ef638e1cde90275ce7c0e12fc4902c27bcbdeefd',
            submodules=True)
    version('3.0.0', commit='b36b1673b2c6b7ff3126d8261bef0f8f176c7beb',
            submodules=True)

    variant('shared', default=True, description='Build shared libraries')
    variant('static', default=False, description='Build static libraries')
    variant('python', default=False, description='Enable Python support')
    variant('python_deps', default=False,
            description='Install non-critical python dependencies '
                        '(may significantly increase spack install time)')
    variant('mpi', default=False,
            description='Enable support for MPI aggregation')
    variant('nccl', default=False,
            description='Enable support for wrapping NCCL functions')
    variant('tau', default=False, description='Enable TAU support')
    variant('papi', default=False, description='Enable PAPI support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('cupti', default=False, description='Enable CUPTI support')
    variant('tools', default=True, description='Build/install extra tools')
    variant('vtune', default=False, description='Enable VTune support')
    variant('upcxx', default=False, description='Enable UPC++ support')
    variant('gotcha', default=False, description='Enable GOTCHA support')
    variant('likwid', default=False, description='Enable LIKWID support')
    variant('caliper', default=False, description='Enable Caliper support')
    variant('dyninst', default=False,
            description='Build dynamic instrumentation tools')
    variant('examples', default=False, description='Build/install examples')
    variant('gperftools', default=False,
            description='Enable gperftools support')
    variant('kokkos_tools', default=False,
            description=('Build generic kokkos-tools libraries, e.g. '
                         'kp_timemory, kp_timemory_filter'))
    variant('kokkos_build_config', default=False,
            description=('Build pre-configured (i.e. dedicated) kokkos-tools '
                         'libraries, e.g. kp_timemory_cpu_flops'))
    variant('cuda_arch', default='auto', description='CUDA architecture name',
            values=('auto', 'kepler', 'tesla', 'maxwell', 'pascal',
                    'volta', 'turing'), multi=False)
    variant('cpu_target', default='auto',
            description=('Build for specific cpu architecture (specify '
                         'cpu-model)'))
    variant('use_arch', default=False,
            description=('Build all of timemory w/ cpu_target architecture '
                         'flags (default: roofline toolkit only)'))
    variant('tls_model', default='global-dynamic',
            description='Thread-local static model', multi=False,
            values=('global-dynamic', 'local-dynamic', 'initial-exec',
                    'local-exec'))
    variant('lto', default=False,
            description='Build w/ link-time optimization')
    variant('statistics', default=True,
            description=('Build components w/ support for statistics '
                         '(min/max/stddev)'))
    variant('extra_optimizations', default=True,
            description='Build timemory with extra optimization flags')
    variant('cxxstd', default='14', description='C++ language standard',
            values=('14', '17', '20'), multi=False)
    variant('mpip_library', default=False,
            description='Build stand-alone timemory-mpip GOTCHA library')
    variant('ompt', default=False, description=('Enable OpenMP tools support'))
    variant('ompt_standalone', default=False,
            description=('Enable OpenMP tools support via drop-in '
                         'replacement of libomp/libgomp/libiomp5'))
    variant('ompt_llvm', default=False,
            description='Enable OpenMP tools support as part of llvm build')
    variant('ompt_library', default=False,
            description='Build stand-alone timemory-ompt library')
    variant('allinea_map', default=False,
            description='Enable Allinea ARM-MAP support')
    variant('require_packages', default=True,
            description=('find_package(...) resulting in NOTFOUND '
                         'generates error'))

    depends_on('cmake@3.11:', type='build')

    extends('python', when='+python')
    depends_on('python@3:', when='+python', type=('build', 'run'))
    depends_on('py-cython', when='+python', type=('build'))
    depends_on('pil', when='+python+python_deps', type=('run'))
    depends_on('py-numpy', when='+python+python_deps', type=('run'))
    depends_on('py-matplotlib', when='+python+python_deps', type=('run'))
    depends_on('py-ipython', when='+python+python_deps', type=('run'))
    depends_on('py-mpi4py', when='+python+mpi+python_deps', type=('run'))
    depends_on('mpi', when='+mpi')
    depends_on('nccl', when='+nccl')
    depends_on('tau', when='+tau')
    depends_on('papi', when='+papi')
    depends_on('cuda', when='+cuda')
    depends_on('cuda', when='+cupti')
    depends_on('upcxx', when='+upcxx')
    depends_on('likwid', when='+likwid')
    depends_on('gotcha', when='+gotcha')
    depends_on('caliper', when='+caliper')
    depends_on('dyninst', when='+dyninst')
    depends_on('gperftools', when='+gperftools')
    depends_on('intel-parallel-studio', when='+vtune')
    depends_on('llvm-openmp-ompt+standalone', when='+ompt_standalone')
    depends_on('llvm-openmp-ompt~standalone', when='+ompt_llvm')
    depends_on('arm-forge', when='+allinea_map')

    conflicts('+python', when='~shared',
              msg='+python requires building shared libraries')
    conflicts('+python_deps', when='~python')
    conflicts('+cupti', when='~cuda', msg='CUPTI requires CUDA')
    conflicts('+kokkos_tools', when='~tools',
              msg='+kokkos_tools requires +tools')
    conflicts('+kokkos_build_config', when='~tools',
              msg='+kokkos_build_config requires +tools')
    conflicts('+kokkos_build_config', when='~kokkos_tools',
              msg='+kokkos_build_config requires +kokkos_tools')
    conflicts('tls_model=local-dynamic', when='+python',
              msg='+python require tls_model=global-dynamic')
    conflicts('tls_model=initial-exec', when='+python',
              msg='+python require tls_model=global-dynamic')
    conflicts('tls_model=local-exec', when='+python',
              msg='+python require tls_model=global-dynamic')
    conflicts('+nccl', when='~gotcha',
              msg='+nccl requires +gotcha')
    conflicts('+mpip_library', when='~mpi', msg='+mpip_library requires +mpi')
    conflicts('+mpip_library', when='~gotcha',
              msg='+mpip_library requires +gotcha')
    conflicts('+mpip_library', when='~shared',
              msg='+mpip_library requires building shared libraries')
    conflicts('+ompt_standalone', when='~ompt',
              msg='+ompt_standalone requires +ompt')
    conflicts('+ompt_llvm', when='~ompt',
              msg='+ompt_llvm requires +ompt')
    conflicts('+ompt_library', when='~ompt',
              msg='+ompt_library requires +ompt')
    conflicts('+ompt_library', when='~shared~static',
              msg='+ompt_library requires building shared or static libraries')
    conflicts('+ompt_standalone+ompt_llvm',
              msg=('+ompt_standalone and +ompt_llvm are not compatible. Use '
                   '+ompt_llvm~ompt_standalone if building LLVM, use '
                   '~ompt_llvm+ompt_standalone if ompt.h is not provided by '
                   'the compiler'))

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DTIMEMORY_BUILD_PYTHON=ON',
            '-DTIMEMORY_BUILD_TESTING=OFF',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON',
        ]

        cxxstd = spec.variants['cxxstd'].value
        args.append('-DCMAKE_CXX_STANDARD={0}'.format(cxxstd))

        tls = spec.variants['tls_model'].value
        args.append('-DTIMEMORY_TLS_MODEL={0}'.format(tls))

        if '+python' in spec:
            args.append('-DPYTHON_EXECUTABLE={0}'.format(
                spec['python'].command.path))

        if '+nccl' in spec:
            args.append('-DTIMEMORY_USE_NCCL=ON')
            args.append('-DTIMEMORY_BUILD_NCCLP_LIBRARY=ON')

        if '+mpi' in spec:
            args.append('-DTIMEMORY_USE_MPI_LINK_FLAGS=OFF')
            args.append('-DMPI_C_COMPILER={0}'.format(spec['mpi'].mpicc))
            args.append('-DMPI_CXX_COMPILER={0}'.format(spec['mpi'].mpicxx))

        if '+cuda' in spec:
            targ = spec.variants['cuda_arch'].value
            key = '' if spec.satisfies('@:3.0.1') else 'TIMEMORY_'
            # newer versions use 'TIMEMORY_CUDA_ARCH'
            args.append('-D{0}CUDA_ARCH={1}'.format(key, targ))

        cpu_target = spec.variants['cpu_target'].value
        if cpu_target == 'auto':
            args.append('-DCpuArch_TARGET={0}'.format(cpu_target))

        # forced disabling of submodule builds
        for dep in ('caliper', 'gotcha', 'ompt'):
            args.append('-DTIMEMORY_BUILD_{0}=OFF'.format(dep.upper()))

        # spack options which translate to TIMEMORY_<OPTION>
        for dep in ('require_packages', 'kokkos_build_config', 'use_arch'):
            args.append('-DTIMEMORY_{0}={1}'.format(
                dep.upper(), 'ON' if '+{0}'.format(dep) in spec else 'OFF'))

        # spack options which translate to BUILD_<OPTION>_LIBS
        for dep in ('shared', 'static'):
            args.append('-DBUILD_{0}_LIBS={1}'.format(
                dep.upper(), 'ON' if '+{0}'.format(dep) in spec else 'OFF'))

        # spack options which translate to TIMEMORY_BUILD_<OPTION>
        for dep in ('tools', 'examples', 'kokkos_tools', 'lto',
                    'extra_optimizations', 'mpip_library', 'ompt_library'):
            args.append('-DTIMEMORY_BUILD_{0}={1}'.format(
                dep.upper(), 'ON' if '+{0}'.format(dep) in spec else 'OFF'))

        # spack options which translate to TIMEMORY_USE_<OPTION>
        for dep in ('allinea_map', 'python', 'mpi', 'tau', 'papi', 'ompt',
                    'cuda', 'cupti', 'cupti', 'vtune', 'upcxx', 'gotcha',
                    'likwid', 'caliper', 'dyninst', 'gperftools',
                    'statistics'):
            args.append('-DTIMEMORY_USE_{0}={1}'.format(
                dep.upper(), 'ON' if '+{0}'.format(dep) in spec else 'OFF'))

        return args
