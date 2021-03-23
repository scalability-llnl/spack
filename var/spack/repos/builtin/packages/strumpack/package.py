# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.environment import set_env
from spack.util.executable import which


class Strumpack(CMakePackage, CudaPackage, ROCmPackage):
    """STRUMPACK -- STRUctured Matrix PACKage - provides linear solvers
    for sparse matrices and for dense rank-structured matrices, i.e.,
    matrices that exhibit some kind of low-rank property. It provides a
    distributed memory fully algebraic sparse solver and
    preconditioner. The preconditioner is mostly aimed at large sparse
    linear systems which result from the discretization of a partial
    differential equation, but is not limited to any particular type of
    problem. STRUMPACK also provides preconditioned GMRES and BiCGStab
    iterative solvers."""

    homepage = "http://portal.nersc.gov/project/sparse/strumpack"
    url      = "https://github.com/pghysels/STRUMPACK/archive/v5.1.0.tar.gz"
    git      = "https://github.com/pghysels/STRUMPACK.git"

    maintainers = ['pghysels']

    test_requires_compiler = True

    version('master', branch='master')
    version('5.1.1', sha256='6cf4eaae5beb9bd377f2abce9e4da9fd3e95bf086ae2f04554fad6dd561c28b9')
    version('5.0.0', sha256='bdfd1620ff7158d96055059be04ee49466ebaca8213a2fdab33e2d4571019a49')
    version('4.0.0', sha256='a3629f1f139865c74916f8f69318f53af6319e7f8ec54e85c16466fd7d256938')
    version('3.3.0', sha256='499fd3b58656b4b6495496920e5372895861ebf15328be8a7a9354e06c734bc7')
    version('3.2.0', sha256='34d93e1b2a3b8908ef89804b7e08c5a884cbbc0b2c9f139061627c0d2de282c1')
    version('3.1.1', sha256='c1c3446ee023f7b24baa97b24907735e89ce4ae9f5ef516645dfe390165d1778')

    variant('shared', default=False, description='Build shared libraries')
    variant('mpi', default=True, description='Use MPI')
    variant('openmp', default=True,
            description='Enable thread parallellism via tasking with OpenMP')
    variant('parmetis', default=True,
            description='Enable use of ParMetis')
    variant('scotch', default=False,
            description='Enable use of Scotch')
    variant('butterflypack', default=True,
            description='Enable use of ButterflyPACK')
    variant('zfp', default=True,
            description='Build with support for compression using ZFP')
    variant('c_interface', default=True,
            description='Enable C interface')
    variant('count_flops', default=False,
            description='Build with flop counters')
    variant('task_timers', default=False,
            description='Build with timers for internal routines')
    variant('build_dev_tests', default=False,
            description='Build developer test routines')
    variant('build_tests', default=False,
            description='Build test routines')
    variant('slate', default=True,
            description="Build with SLATE support")

    depends_on('cmake@3.11:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack', when='+mpi')
    depends_on('metis')
    depends_on('parmetis', when='+parmetis')
    depends_on('scotch~metis', when='+scotch')
    depends_on('scotch~metis+mpi', when='+scotch+mpi')
    depends_on('butterflypack@1.1.0', when='@3.3.0:3.9.999 +butterflypack+mpi')
    depends_on('butterflypack@1.2.0:', when='@4.0.0: +butterflypack+mpi')
    depends_on('cuda', when='@4.0.0: +cuda')
    depends_on('zfp', when='+zfp')
    depends_on('hipblas', when='+rocm')
    depends_on('rocsolver', when='+rocm')
    depends_on('slate', when='+slate')
    depends_on('slate+cuda', when='+cuda+slate')

    conflicts('+parmetis', when='~mpi')
    conflicts('+butterflypack', when='~mpi')
    conflicts('+butterflypack', when='@:3.2.0')
    conflicts('+zfp', when='@:3.9.999')
    conflicts('+cuda', when='@:3.9.999')
    conflicts('+rocm', when='@:5.0.999')
    conflicts('+rocm', when='+cuda')
    conflicts('+slate', when='@:5.1.1')
    conflicts('+slate', when='~mpi')
    conflicts('^openblas@0.3.6: threads=none', when='+openmp',
              msg='STRUMPACK requires openblas with OpenMP threading support')
    conflicts('^openblas@0.3.6: threads=pthreads', when='+openmp',
              msg='STRUMPACK requires openblas with OpenMP threading support')

    patch('intel-19-compile.patch', when='@3.1.1')

    def cmake_args(self):
        spec = self.spec

        def on_off(varstr):
            return 'ON' if varstr in spec else 'OFF'

        args = [
            '-DSTRUMPACK_USE_MPI=%s' % on_off('+mpi'),
            '-DSTRUMPACK_USE_OPENMP=%s' % on_off('+openmp'),
            '-DSTRUMPACK_USE_CUDA=%s' % on_off('+cuda'),
            '-DSTRUMPACK_USE_HIP=%s' % on_off('+rocm'),
            '-DTPL_ENABLE_PARMETIS=%s' % on_off('+parmetis'),
            '-DTPL_ENABLE_SCOTCH=%s' % on_off('+scotch'),
            '-DTPL_ENABLE_BPACK=%s' % on_off('+butterflypack'),
            '-DSTRUMPACK_COUNT_FLOPS=%s' % on_off('+count_flops'),
            '-DSTRUMPACK_TASK_TIMERS=%s' % on_off('+task_timers'),
            '-DSTRUMPACK_DEV_TESTING=%s' % on_off('+build_dev_tests'),
            '-DSTRUMPACK_BUILD_TESTS=%s' % on_off('+build_tests'),
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DBUILD_SHARED_LIBS=%s' % on_off('+shared')
        ]

        if '+mpi' in spec:
            args.append(
                '-DTPL_SCALAPACK_LIBRARIES=%s' % spec['scalapack'].
                libs.joined(";"))

        if spec.satisfies('@:3.9.999'):
            if '+mpi' in spec:
                args.extend([
                    '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
                    '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
                    '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc
                ])
            args.extend([
                '-DSTRUMPACK_C_INTERFACE=%s' % on_off('+c_interface'),
            ])

        if '+cuda' in spec:
            args.extend([
                '-DCUDA_TOOLKIT_ROOT_DIR={0}'.format(spec['cuda'].prefix),
                '-DCMAKE_CUDA_HOST_COMPILER={0}'.format(env["SPACK_CXX"])])
            cuda_archs = spec.variants['cuda_arch'].value
            if 'none' not in cuda_archs:
                args.append('-DCUDA_NVCC_FLAGS={0}'.
                            format(' '.join(self.cuda_flags(cuda_archs))))

        if '+rocm' in spec:
            args.append(
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix))
            rocm_archs = spec.variants['amdgpu_target'].value
            if 'none' not in rocm_archs:
                args.append('-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.
                            format(",".join(rocm_archs)))

        return args

    test_data_dir = 'examples/data'
    test_src_dir = 'test'

    @run_after('install')
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources([self.test_data_dir, self.test_src_dir])

    def _test_example(self, test_prog, test_dir, test_cmd, test_args):
        tmpbld_dir = '{0}/_BUILD'.format(test_dir)
        with working_dir(tmpbld_dir, create=True):
            with open('{0}/CMakeLists.txt'.format(tmpbld_dir), 'w') as mkfile:
                mkfile.write('cmake_minimum_required(VERSION 3.13)\n')
                mkfile.write('project(StrumpackSmokeTest LANGUAGES CXX)\n')
                mkfile.write('find_package(STRUMPACK REQUIRED)\n')
                mkfile.write('add_executable({0} ../{0}.cpp)\n'.
                             format(test_prog))
                mkfile.write('target_link_libraries({0} '.format(test_prog) +
                             'PRIVATE STRUMPACK::strumpack)\n')

            opts = self.std_cmake_args
            opts += self.cmake_args()
            opts += ['.']
            self.run_test('cmake', opts, [], installed=False, work_dir='.')
            self.run_test('make')
            with set_env(OMP_NUM_THREADS='4'):
                self.run_test(test_cmd, test_args, installed=False,
                              purpose='test: strumpack smoke test',
                              skip_missing=False, work_dir='.')
        self.run_test('rm', ['-fR', tmpbld_dir])

    def test(self):
        test_dir = join_path(self.install_test_root, self.test_src_dir)
        test_exe = 'test_sparse_seq'
        test_exe_mpi = 'test_sparse_mpi'
        exe_arg = ['../../examples/data/pde900.mtx']
        if '+mpi' in self.spec:
            test_args = ['-n', '4', test_exe_mpi]
            test_args.extend(exe_arg)
            mpiexe_list = ['mpirun', 'mpiexec', 'srun']
            for mpiexe in mpiexe_list:
                if which(mpiexe) is not None:
                    self._test_example(test_exe_mpi, test_dir,
                                       mpiexe, test_args)
                    break
        else:
            self._test_example(test_exe, test_dir, test_exe, exe_arg)
