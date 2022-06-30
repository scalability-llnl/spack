# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack.package import *


class Omnitrace(CMakePackage):
    '''Application Profiling, Tracing, and Analysis'''

    homepage = 'https://amdresearch.github.io/omnitrace'
    git = 'https://github.com/AMDResearch/omnitrace.git'
    maintainers = ['jrmadsen']

    version('main', branch='main', submodules=True)
    version('1.2.0', commit='f82845388aab108ed1d1fc404f433a0def391bb3', submodules=True)

    variant(
        'rocm', default=True, description='Enable ROCm API and kernel tracing support'
    )
    variant(
        'strip',
        default=False,
        description="Faster binary instrumentation, worse debugging",
    )
    variant('python', default=False, description='Enable Python support')
    variant('papi', default=True, description='Enable PAPI support')
    variant('ompt', default=True, description='Enable OpenMP Tools support')
    variant('tau', default=False, description='Enable TAU support')
    variant('caliper', default=False, description='Enable Caliper support')
    variant(
        'perfetto_tools',
        default=False,
        description='Install perfetto tools (e.g. traced, perfetto)',
    )
    variant(
        'mpi',
        default=False,
        description=' '.join(
            [
                'Enable intercepting MPI functions and aggregating output',
                'during finalization (requires target application to use',
                'same MPI installation)',
            ]
        ),
    )
    variant(
        'mpi_headers',
        default=True,
        description=' '.join(
            [
                'Enable intercepting MPI functions but w/o support for aggregating',
                'output (target application can use any MPI installation)',
            ]
        ),
    )

    extends('python', when='+python')

    # hard dependencies
    depends_on('cmake@3.16:', type='build')
    depends_on('dyninst@11.0.1:', type=('build', 'run'))
    depends_on('libunwind', type=('build', 'run'))

    # soft dependencies
    depends_on('hip', when='+rocm')
    depends_on('rocm-smi-lib', when='+rocm')
    depends_on('roctracer-dev', when='+rocm')
    depends_on('papi+shared', when='+papi')
    depends_on('mpi', when='+mpi')
    depends_on('tau', when='+tau')
    depends_on('caliper', when='+caliper')
    depends_on('python@3:', when='+python', type=('build', 'run'))

    def __init__(self, *args, **kwargs):
        super(Omnitrace, self).__init__(*args, **kwargs)
        # default to a release build
        self.variants["build_type"][0].default = "Release"

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define('SPACK_BUILD', True),
            self.define('OMNITRACE_BUILD_PAPI', False),
            self.define('OMNITRACE_BUILD_PYTHON', True),
            self.define('OMNITRACE_BUILD_DYNINST', False),
            self.define('OMNITRACE_BUILD_LIBUNWIND', False),
            self.define('OMNITRACE_BUILD_STATIC_LIBGCC', False),
            self.define('OMNITRACE_BUILD_STATIC_LIBSTDCXX', False),
            self.define_from_variant('OMNITRACE_BUILD_LTO', 'ipo'),
            self.define_from_variant('OMNITRACE_USE_HIP', 'rocm'),
            self.define_from_variant('OMNITRACE_USE_MPI', 'mpi'),
            self.define_from_variant('OMNITRACE_USE_OMPT', 'ompt'),
            self.define_from_variant('OMNITRACE_USE_PAPI', 'papi'),
            self.define_from_variant('OMNITRACE_USE_ROCM_SMI', 'rocm'),
            self.define_from_variant('OMNITRACE_USE_ROCTRACER', 'rocm'),
            self.define_from_variant('OMNITRACE_USE_PYTHON', 'python'),
            self.define_from_variant('OMNITRACE_USE_MPI_HEADERS', 'mpi_headers'),
            self.define_from_variant(
                'OMNITRACE_INSTALL_PERFETTO_TOOLS', 'perfetto_tools'
            ),
            self.define_from_variant('OMNITRACE_STRIP_LIBRARIES', 'strip'),
            # timemory arguments
            self.define('TIMEMORY_UNITY_BUILD', False),
            self.define('TIMEMORY_BUILD_CALIPER', False),
            self.define_from_variant('TIMEMORY_USE_TAU', 'tau'),
            self.define_from_variant('TIMEMORY_USE_CALIPER', 'caliper'),
        ]

        if "+tau" in spec:
            tau_root = spec['tau'].prefix
            args.append(self.define('TAU_ROOT_DIR', tau_root))

        if '+python' in spec:
            pyexe = spec['python'].command.path
            args.append(self.define('PYTHON_EXECUTABLE', pyexe))
            args.append(self.define('Python3_EXECUTABLE', pyexe))

        if '+mpi' in spec:
            args.append(self.define('MPI_C_COMPILER', spec['mpi'].mpicc))
            args.append(self.define('MPI_CXX_COMPILER', spec['mpi'].mpicxx))

        return args

    def setup_run_environment(self, env):
        if "+python" in self.spec:
            env.prepend_path(
                "PYTHONPATH", join_path(self.prefix.lib, "python", "site-packages")
            )
