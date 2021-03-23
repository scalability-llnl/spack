# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import sys


class Hpx(CMakePackage, CudaPackage):
    """C++ runtime system for parallel and distributed applications."""

    homepage = "https://hpx.stellar-group.org/"
    url = "https://github.com/STEllAR-GROUP/hpx/archive/1.2.1.tar.gz"
    maintainers = ['msimberg', 'albestro', 'teonnik']

    version('master', git='https://github.com/STEllAR-GROUP/hpx.git', branch='master')
    version('stable', git='https://github.com/STEllAR-GROUP/hpx.git', tag='stable')
    version('1.6.0', sha256='4ab715613c1e1808edc93451781cc9bc98feec4e422ccd4322858a680f6d9017')
    version('1.5.1', sha256='b2f9358ce2a9446b9d8fb1998c30913e7199b007aa82e46d0aa05c763331c635')
    version('1.5.0', sha256='de2901d8ae017592c513e0af9cf58de295abc9802e55ece00424cbd8a3801920')
    version('1.4.1', sha256='965dabe44d17480e326d92da4eec56722d98b33943c53d2b0f8f4655cb208023')
    version('1.4.0', sha256='241a1c47fafba751848fac12446e7bf4ad3d342d5eb2fa1ef94dd904acc329ed')
    version('1.3.0', sha256='cd34da674064c4cc4a331402edbd65c5a1f8058fb46003314ca18fa08423c5ad')
    version('1.2.1', sha256='8cba9b48e919035176d3b7bbfc2c110df6f07803256626f1dad8d9dde16ab77a')
    version('1.2.0', sha256='20942314bd90064d9775f63b0e58a8ea146af5260a4c84d0854f9f968077c170')
    version('1.1.0', sha256='1f28bbe58d8f0da600d60c3a74a644d75ac777b20a018a5c1c6030a470e8a1c9')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            description='Use the specified C++ standard when building.')

    variant(
        'malloc', default='tcmalloc',
        description='Define which allocator will be linked in',
        values=('system', 'tcmalloc', 'jemalloc', 'tbbmalloc')
    )

    variant('max_cpu_count', default='64',
            description='Max number of OS-threads for HPX applications',
            values=lambda x: isinstance(x, str) and x.isdigit())

    variant('instrumentation', values=any_combination_of(
        'apex', 'google_perftools', 'papi', 'valgrind'
    ), description='Add support for various kind of instrumentation')

    variant(
        "networking",
        values=any_combination_of("tcp", "mpi").with_default("tcp"),
        description="Support for networking through parcelports",
    )

    default_generic_coroutines = True
    if sys.platform.startswith('linux') or sys.platform == 'win32':
        default_generic_coroutines = False
    variant(
        "generic_coroutines", default=default_generic_coroutines,
        description='Use Boost.Context as the underlying coroutines'
                    ' context switch implementation.')

    variant('tools', default=False, description='Build HPX tools')
    variant('examples', default=False, description='Build examples')
    variant('async_mpi', default=False, description='Enable MPI Futures.')
    variant('async_cuda', default=False, description='Enable CUDA Futures.')

    depends_on('hwloc')
    depends_on('python', type=('build', 'test', 'run'))
    depends_on('pkgconfig', type='build')
    depends_on('git', type='build')

    # Recommended dependency versions for 1.2.X
    depends_on('cmake@3.9.0:', when='@:1.2.1', type='build')
    depends_on('boost@1.62.0:', when='@:1.2.1')
    depends_on('hwloc@1.11:', when='@:1.2.1')

    # Recommended dependency versions before 1.2
    depends_on('boost@1.55.0:', when='@:1.1.0')
    depends_on('hwloc@1.6:', when='@:1.1.0')

    # boost 1.73.0 build problem with HPX 1.4.0 and 1.4.1
    # https://github.com/STEllAR-GROUP/hpx/issues/4728#issuecomment-640685308
    depends_on('boost@:1.72.0', when='@:1.4')

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on('boost+context', when='+generic_coroutines')
    _msg_generic_coroutines = 'This platform requires +generic_coroutines'
    conflicts('~generic_coroutines', when='platform=darwin', msg=_msg_generic_coroutines)

    # CXX Standard
    depends_on('boost cxxstd=11', when='cxxstd=11')
    depends_on('boost cxxstd=14', when='cxxstd=14')
    depends_on('boost cxxstd=17', when='cxxstd=17')

    # Malloc
    depends_on('gperftools', when='malloc=tcmalloc')
    depends_on('jemalloc', when='malloc=jemalloc')
    depends_on('tbb', when='malloc=tbbmalloc')

    # MPI
    depends_on('mpi', when='networking=mpi')
    depends_on('mpi', when='+async_mpi')

    # CUDA
    depends_on('cuda', when='+async_cuda')

    # Instrumentation
    depends_on('otf2', when='instrumentation=apex')
    depends_on('gperftools', when='instrumentation=google_perftools')
    depends_on('papi', when='instrumentation=papi')
    depends_on('valgrind', when='instrumentation=valgrind')

    # Patches APEX
    patch('git_external.patch', when='@1.3.0 instrumentation=apex')

    def instrumentation_args(self):
        for value in self.variants['instrumentation'].values:
            if value == 'none':
                continue

            condition = 'instrumentation={0}'.format(value)
            yield self.define(
                'HPX_WITH_{0}'.format(value.upper()), condition in self.spec)

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define(
                'HPX_WITH_CXX{0}'.format(spec.variants['cxxstd'].value), True),

            self.define_from_variant('HPX_WITH_MALLOC', 'malloc'),
            self.define_from_variant('HPX_WITH_CUDA', 'cuda'),
            self.define_from_variant('HPX_WITH_TOOLS', 'tools'),
            self.define_from_variant('HPX_WITH_EXAMPLES', 'examples'),
            self.define_from_variant('HPX_WITH_ASYNC_MPI', 'async_mpi'),
            self.define_from_variant('HPX_WITH_ASYNC_CUDA', 'async_cuda'),
            self.define('HPX_WITH_TESTS', self.run_tests),

            self.define('HPX_WITH_NETWORKING', 'networking=none' not in spec),
            self.define('HPX_WITH_PARCELPORT_TCP', 'networking=tcp' in spec),
            self.define('HPX_WITH_PARCELPORT_MPI', 'networking=mpi' in spec),

            self.define_from_variant(
                'HPX_WITH_MAX_CPU_COUNT', 'max_cpu_count'),
            self.define_from_variant(
                'HPX_WITH_GENERIC_CONTEXT_COROUTINES', 'generic_coroutines'),

            self.define('BOOST_ROOT', spec['boost'].prefix),
            self.define('HWLOC_ROOT', spec['hwloc'].prefix),
            self.define('HPX_WITH_BOOST_ALL_DYNAMIC_LINK', True),
            self.define('BUILD_SHARED_LIBS', True),
            self.define('HPX_DATASTRUCTURES_WITH_ADAPT_STD_TUPLE', False),
        ]

        # Instrumentation
        args += self.instrumentation_args()

        if 'instrumentation=apex' in spec:
            args += [
                self.define('APEX_WITH_OTF2', True),
                self.define('OTF2_ROOT', spec['otf2'].prefix),
            ]

            # it seems like there was a bug in the default version of APEX in 1.5.x
            if spec.satisfies("@1.5"):
                args += [self.define('HPX_WITH_APEX_TAG', "v2.3.0")]

        return args
