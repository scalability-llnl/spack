# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

import socket
import os
import shutil

from os import environ as env
from os.path import join as pjoin

#TODO (bernede1@llnl.gov):
# - no mesquite dep
# - no direct parmetis
# - no mumps
# - no direct scotch
# - no direct scalapack

def cmake_cache_entry(name, value, comment=""):
    """Generate a string for a cmake cache variable"""

    return 'set(%s "%s" CACHE PATH "%s")\n\n' % (name,value,comment)

def cmake_cache_string(name, string, comment=""):
    """Generate a string for a cmake cache variable"""

    return 'set(%s "%s" CACHE STRING "%s")\n\n' % (name,string,comment)

def cmake_cache_option(name, boolean_value, comment=""):
    """Generate a string for a cmake configuration option"""

    value = "ON" if boolean_value else "OFF"
    return 'set(%s %s CACHE BOOL "%s")\n\n' % (name,value,comment)


def get_spec_path(spec, package_name, path_replacements = {}, use_bin = False) :
    """Extracts the prefix path for the given spack package
       path_replacements is a dictionary with string replacements for the path.
    """

    if not use_bin:
        path = spec[package_name].prefix
    else:
        path = spec[package_name].prefix.bin

    path = os.path.realpath(path)

    for key in path_replacements:
        path = path.replace(key, path_replacements[key])

    return path


def path_replace(path, path_replacements):
    """Replaces path key/value pairs from path_replacements in path"""
    for key in path_replacements:
        path = path.replace(key,path_replacements[key])
    return path


class MfemCmake(CMakePackage, CudaPackage):
    """Free, lightweight, scalable C++ library for finite element methods."""

    tags = ['FEM', 'finite elements', 'high-order', 'AMR', 'HPC']

    homepage = 'http://www.mfem.org'
    git      = 'https://github.com/mfem/mfem.git'

    maintainers = ['v-dobrev', 'tzanio', 'acfisher',
                   'goxberry', 'markcmiller86']

    # Recommended mfem builds to test when updating this file: see the shell
    # script 'test_builds.sh' in the same directory as this file.

    # mfem is downloaded from a URL shortener at request of upstream
    # author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    #     https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    http://mfem.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://mfem.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    # 'develop' is a special version that is always larger (or newer) than any
    # other version.
    version('develop', branch='master')

    version('4.2.0',
            '4352a225b55948d2e73a5ee88cece0e88bdbe7ba6726a23d68b2736d3221a86d',
            url='https://bit.ly/mfem-4-2', extension='tar.gz',
            preferred=True)

    version('4.1.0',
            '4c83fdcf083f8e2f5b37200a755db843cdb858811e25a8486ad36b2cbec0e11d',
            url='https://bit.ly/mfem-4-1', extension='tar.gz')

    # Tagged development version used by xSDK
    version('4.0.1-xsdk', commit='c55c80d17b82d80de04b849dd526e17044f8c99a')

    version('4.0.0',
            'df5bdac798ea84a263979f6fbf79de9013e1c55562f95f98644c3edcacfbc727',
            url='https://bit.ly/mfem-4-0', extension='tar.gz')

    # Tagged development version used by the laghos package:
    version('3.4.1-laghos-v2.0', tag='laghos-v2.0')

    version('3.4.0',
            sha256='4e73e4fe0482636de3c5dc983cd395839a83cb16f6f509bd88b053e8b3858e05',
            url='https://bit.ly/mfem-3-4', extension='tar.gz')

    version('3.3.2',
            sha256='b70fa3c5080b9ec514fc05f4a04ff74322b99ac4ecd6d99c229f0ed5188fc0ce',
            url='https://goo.gl/Kd7Jk8', extension='tar.gz')

    # Tagged development version used by the laghos package:
    version('3.3.1-laghos-v1.0', tag='laghos-v1.0')

    version('3.3',
            sha256='b17bd452593aada93dc0fee748fcfbbf4f04ce3e7d77fdd0341cc9103bcacd0b',
            url='http://goo.gl/Vrpsns', extension='tar.gz')

    version('3.2',
            sha256='2938c3deed4ec4f7fd5b5f5cfe656845282e86e2dcd477d292390058b7b94340',
            url='http://goo.gl/Y9T75B', extension='tar.gz')

    version('3.1',
            sha256='841ea5cf58de6fae4de0f553b0e01ebaab9cd9c67fa821e8a715666ecf18fc57',
            url='http://goo.gl/xrScXn', extension='tar.gz')

    variant('static', default=True,
            description='Build static library')
    variant('shared', default=False,
            description='Build shared library')
    variant('mpi', default=True,
            description='Enable MPI parallelism')
    # Can we make the default value for 'metis' to depend on the 'mpi' value?
    variant('metis', default=True,
            description='Enable METIS support')
    variant('openmp', default=False,
            description='Enable OpenMP parallelism')
    variant('occa', default=False, description='Enable OCCA backend')
    variant('raja', default=False, description='Enable RAJA backend')
    variant('libceed', default=False, description='Enable libCEED backend')
    variant('umpire', default=False, description='Enable Umpire support')
    variant('amgx', default=False, description='Enable NVIDIA AmgX solver support')

    variant('threadsafe', default=False,
            description=('Enable thread safe features.'
                         ' Required for OpenMP.'
                         ' May cause minor performance issues.'))
    variant('superlu-dist', default=False,
            description='Enable MPI parallel, sparse direct solvers')
    variant('strumpack', default=False,
            description='Enable support for STRUMPACK')
    variant('suite-sparse', default=False,
            description='Enable serial, sparse direct solvers')
    variant('petsc', default=False,
            description='Enable PETSc solvers, preconditioners, etc.')
    variant('sundials', default=False,
            description='Enable Sundials time integrators')
    variant('pumi', default=False,
            description='Enable functionality based on PUMI')
    variant('gslib', default=False,
            description='Enable functionality based on GSLIB')
    variant('mpfr', default=False,
            description='Enable precise, 1D quadrature rules')

    variant('lapack', default=False,
            description='Use external blas/lapack routines')
    variant('debug', default=False,
            description='Build debug instead of optimized version')
    variant('netcdf', default=False,
            description='Enable Cubit/Genesis reader')
    variant('conduit', default=False,
            description='Enable binary data I/O using Conduit')
    variant('zlib', default=True,
            description='Support zip\'d streams for I/O')
    variant('gnutls', default=False,
            description='Enable secure sockets using GnuTLS')
    variant('libunwind', default=False,
            description='Enable backtrace on error support using Libunwind')
    # TODO: HIP, SIMD, Ginkgo, SLEPc, ADIOS2, HiOp, MKL CPardiso,
    #       Axom/Sidre
    variant('timer', default='auto',
            values=('auto', 'std', 'posix', 'mac', 'mpi'),
            description='Timing functions to use in mfem::StopWatch')
    variant('examples', default=False,
            description='Build and install examples')
    variant('miniapps', default=False,
            description='Build and install miniapps')

    conflicts('+shared', when='@:3.3.2')
    conflicts('~static~shared')
    conflicts('~threadsafe', when='@:3.99.99+openmp')

    conflicts('+cuda', when='@:3.99.99')
    conflicts('+netcdf', when='@:3.1')
    conflicts('+superlu-dist', when='@:3.1')
    # STRUMPACK support was added in mfem v3.3.2, however, here we allow only
    # strumpack v3+ support for which is available starting with mfem v4.0:
    conflicts('+strumpack', when='@:3.99.99')
    conflicts('+gnutls', when='@:3.1')
    conflicts('+zlib', when='@:3.2')
    conflicts('+mpfr', when='@:3.2')
    conflicts('+petsc', when='@:3.2')
    conflicts('+sundials', when='@:3.2')
    conflicts('+pumi', when='@:3.3.2')
    conflicts('+gslib', when='@:4.0.99')
    conflicts('timer=mac', when='@:3.3.0')
    conflicts('timer=mpi', when='@:3.3.0')
    conflicts('~metis+mpi', when='@:3.3.0')
    conflicts('+metis~mpi', when='@:3.3.0')
    conflicts('+conduit', when='@:3.3.2')
    conflicts('+occa', when='mfem@:3.99.99')
    conflicts('+raja', when='mfem@:3.99.99')
    conflicts('+libceed', when='mfem@:4.0.99')
    conflicts('+umpire', when='mfem@:4.0.99')
    conflicts('+amgx', when='mfem@:4.1.99')
    conflicts('+amgx', when='~cuda')

    conflicts('+superlu-dist', when='~mpi')
    conflicts('+strumpack', when='~mpi')
    conflicts('+petsc', when='~mpi')
    conflicts('+pumi', when='~mpi')
    conflicts('timer=mpi', when='~mpi')

    depends_on('mpi', when='+mpi')
    depends_on('hypre@2.10.0:2.13.99', when='@:3.3.99+mpi')
    depends_on('hypre', when='@3.4:+mpi')

    depends_on('metis', when='+metis')
    depends_on('blas', when='+lapack')
    depends_on('lapack@3.0:', when='+lapack')

    depends_on('sundials@2.7.0', when='@:3.3.0+sundials~mpi')
    depends_on('sundials@2.7.0+mpi+hypre', when='@:3.3.0+sundials+mpi')
    depends_on('sundials@2.7.0:', when='@3.3.2:+sundials~mpi')
    depends_on('sundials@2.7.0:+mpi+hypre', when='@3.3.2:+sundials+mpi')
    depends_on('sundials@5.0.0:', when='@4.0.1-xsdk:+sundials~mpi')
    depends_on('sundials@5.0.0:+mpi+hypre', when='@4.0.1-xsdk:+sundials+mpi')
    depends_on('sundials@5.4.0:+cuda', when='@4.2.0:+sundials+cuda')
    depends_on('pumi@2.2.3', when='@4.2.0:+pumi')
    depends_on('pumi', when='+pumi~shared')
    depends_on('pumi+shared', when='+pumi+shared')
    depends_on('gslib@1.0.5:+mpi', when='+gslib+mpi')
    depends_on('gslib@1.0.5:~mpi~mpiio', when='+gslib~mpi')
    depends_on('suite-sparse', when='+suite-sparse')
    depends_on('superlu-dist', when='+superlu-dist')
    depends_on('strumpack@3.0.0:', when='+strumpack~shared')
    depends_on('strumpack@3.0.0:+shared', when='+strumpack+shared')
    # The PETSc tests in MFEM will fail if PETSc is not configured with
    # SuiteSparse and MUMPS. On the other hand, if we require the variants
    # '+suite-sparse+mumps' of PETSc, the xsdk package concretization fails.
    depends_on('petsc@3.8:+mpi+double+hypre', when='+petsc')
    # Recommended when building outside of xsdk:
    # depends_on('petsc@3.8:+mpi+double+hypre+suite-sparse+mumps',
    #            when='+petsc')
    depends_on('mpfr', when='+mpfr')
    depends_on('netcdf-c@4.1.3:', when='+netcdf')
    depends_on('unwind', when='+libunwind')
    depends_on('zlib', when='+zlib')
    depends_on('gnutls', when='+gnutls')
    depends_on('conduit@0.3.1:,master:', when='+conduit')
    depends_on('conduit+mpi', when='+conduit+mpi')

    # The MFEM 4.0.0 SuperLU interface fails when using hypre@2.16.0 and
    # superlu-dist@6.1.1. See https://github.com/mfem/mfem/issues/983.
    # This issue was resolved in v4.1.
    conflicts('+superlu-dist',
              when='mfem@:4.0.99 ^hypre@2.16.0: ^superlu-dist@6:')
    # The STRUMPACK v3 interface in MFEM seems to be broken as of MFEM v4.1
    # when using hypre version >= 2.16.0.
    # This issue is resolved in v4.2.
    conflicts('+strumpack', when='mfem@4.0.0:4.1.99 ^hypre@2.16.0:')
    conflicts('+strumpack ^strumpack+cuda', when='~cuda')

    depends_on('occa@1.0.8:', when='@:4.1.99+occa')
    depends_on('occa@1.1.0:', when='@4.2.0:+occa')
    depends_on('occa+cuda', when='+occa+cuda')

    depends_on('raja@0.10.0:', when='@4.0.1:+raja')
    depends_on('raja@0.7.0:0.9.0', when='@4.0.0+raja')
    depends_on('raja+cuda', when='+raja+cuda')

    depends_on('libceed@0.6:', when='@:4.1.99+libceed')
    depends_on('libceed@0.7:', when='@4.2.0:+libceed')
    depends_on('libceed+cuda', when='+libceed+cuda')

    depends_on('umpire@2.0.0:', when='+umpire')
    depends_on('umpire+cuda', when='+umpire+cuda')

    depends_on('amgx', when='+amgx')
    # MPI is enabled by default
    depends_on('amgx~mpi', when='+amgx~mpi')
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on('amgx cuda_arch={0}'.format(sm_),
                   when='+amgx cuda_arch={0}'.format(sm_))

    patch('mfem_ppc_build.patch', when='@3.2:3.3.0 arch=ppc64le')
    patch('mfem-3.4.patch', when='@3.4.0')
    patch('mfem-3.3-3.4-petsc-3.9.patch',
          when='@3.3.0:3.4.0 +petsc ^petsc@3.9.0:')
    patch('mfem-4.2-umpire.patch', when='@4.2.0+umpire')
    patch('mfem-4.2-netcdf.patch', when='@4.2.0+netcdf')
    # JBE: This is the minimum needed for Serac but probably not sufficient
    # in the general case
    patch('mfem-4.2-static.patch', when='@4.2.0~shared')

    # JBE: Need cuda math libraries to be resolved explicitly
    patch('mfem-4.2-amgx.patch', when='@4.2.0+amgx')

    # Patch to fix MFEM makefile syntax error. See
    # https://github.com/mfem/mfem/issues/1042 for the bug report and
    # https://github.com/mfem/mfem/pull/1043 for the bugfix contributed
    # upstream.
    patch('mfem-4.0.0-makefile-syntax-fix.patch', when='@4.0.0')

    # OLD phases = ['configure', 'build', 'install']
    phases = ['hostconfig', 'cmake', 'build', 'install']

    def setup_build_environment(self, env):
        env.unset('MFEM_DIR')
        env.unset('MFEM_BUILD_DIR')

    def _get_sys_type(self, spec):
        sys_type = str(spec.architecture)
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    def _get_host_config_path(self, spec):
        host_config_path = "hc-%s-%s-%s.cmake" % (socket.gethostname().rstrip('1234567890'),
                                               self._get_sys_type(spec),
                                               spec.format('{name}-{version}-{compiler}-{hash:8}'))
        dest_dir = self.stage.source_path
        host_config_path = os.path.abspath(pjoin(dest_dir, host_config_path))
        return host_config_path

    #
    # Note: Although MFEM does support CMake configuration, MFEM
    # development team indicates that vanilla GNU Make is the
    # preferred mode of configuration of MFEM and the mode most
    # likely to be up to date in supporting *all* of MFEM's
    # configuration options. So, don't use CMake
    #
    def hostconfig(self, spec, prefix):

        def on_off(varstr):
            return True if varstr in spec else False

        # See also find_system_libraries in lib/spack/llnl/util/filesystem.py
        # where the same list of paths is used.
        sys_lib_paths = [
            '/lib64',
            '/lib',
            '/usr/lib64',
            '/usr/lib',
            '/usr/local/lib64',
            '/usr/local/lib']

        def is_sys_lib_path(dir):
            return dir in sys_lib_paths

        # We need to add rpaths explicitly to allow proper export of link flags
        # from within MFEM.

        # Similar to spec[pkg].libs.ld_flags but prepends rpath flags too.
        # Also does not add system library paths as defined by 'sys_lib_paths'
        # above -- this is done to avoid issues like this:
        # https://github.com/mfem/mfem/issues/1088.
        def ld_flags_from_library_list(libs_list):
            flags = ['%s-rpath,%s' % (xlinker, dir)
                     for dir in libs_list.directories
                     if not is_sys_lib_path(dir)]
            flags += ['-L%s' % dir for dir in libs_list.directories
                      if not is_sys_lib_path(dir)]
            flags += [libs_list.link_flags]
            return ' '.join(flags)

        def ld_flags_from_dirs(pkg_dirs_list, pkg_libs_list):
            flags = ['%s-rpath,%s' % (xlinker, dir) for dir in pkg_dirs_list
                     if not is_sys_lib_path(dir)]
            flags += ['-L%s' % dir for dir in pkg_dirs_list
                      if not is_sys_lib_path(dir)]
            flags += ['-l%s' % lib for lib in pkg_libs_list]
            return ' '.join(flags)

        def find_optional_library(name, prefix):
            for shared in [True, False]:
                for path in ['lib64', 'lib']:
                    lib = find_libraries(name, join_path(prefix, path),
                                         shared=shared, recursive=False)
                    if lib:
                        return lib
            return LibraryList([])


        metis5_str = False
        if ('+metis' in spec) and spec['metis'].satisfies('@5:'):
            metis5_str = True

        zlib_var = 'MFEM_USE_ZLIB' if (spec.satisfies('@4.1.0:')) else \
                   'MFEM_USE_GZSTREAM'

        #######################
        # Compiler Info
        #######################
        # By directly fetching the names of the actual compilers we appear
        # to doing something evil here, but this is necessary to create a
        # 'host config' file that works outside of the spack install env.

        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]

        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]

        ##############################################
        # Find and record what CMake is used
        ##############################################

        cmake_exe = spec['cmake'].command.path
        cmake_exe = os.path.realpath(cmake_exe)

        host_config_path = self._get_host_config_path(spec)
        cfg = open(host_config_path, "w")
        cfg.write("####################################################################\n")
        cfg.write("# Generated host-config - Edit at own risk!\n")
        cfg.write("####################################################################\n")
        cfg.write("# Copyright (c) 2019-2020, Lawrence Livermore National Security, LLC and\n")
        cfg.write("# other Serac Project Developers. See the top-level LICENSE file for\n")
        cfg.write("# details.\n")
        cfg.write("#\n")
        cfg.write("# SPDX-License-Identifier: (BSD-3-Clause) \n")
        cfg.write("####################################################################\n\n")

        cfg.write("#---------------------------------------\n")
        cfg.write("# SYS_TYPE: {0}\n".format(sys_type))
        cfg.write("# Compiler Spec: {0}\n".format(spec.compiler))
        cfg.write("# CMake executable path: %s\n" % cmake_exe)
        cfg.write("#---------------------------------------\n\n")

        #######################
        # Compiler Settings
        #######################

        cfg.write("#---------------------------------------\n")
        cfg.write("# Compilers\n")
        cfg.write("#---------------------------------------\n")
        if '+mpi' in spec:
            cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", spec['mpi'].mpicc))
            cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", spec['mpi'].mpicxx))
        else:
            cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", c_compiler))
            cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", cpp_compiler))

        cflags = ' '.join(spec.compiler_flags['cflags'])
        cxxflags = ' '.join(spec.compiler_flags['cxxflags'])

        # Add opt/debug flags if they are not present in global cxx flags
        opt_flag_found = any(f in self.compiler.opt_flags
                             for f in cxxflags)
        debug_flag_found = any(f in self.compiler.debug_flags
                               for f in cxxflags)

        if '+debug' in spec:
            if not debug_flag_found:
                cxxflags = ' '.join([cxxflags,'-g'])
            if not opt_flag_found:
                cxxflags = ' '.join([cxxflags,'-O0'])
        else:
            if not opt_flag_found:
                cxxflags = ' '.join([cxxflags,'-O2'])

        if self.spec.satisfies('@4.0.0:'):
            cxxflags = ' '.join([cxxflags,self.compiler.cxx11_flag])

        if cflags:
            cfg.write(cmake_cache_entry("CMAKE_C_FLAGS", cflags))
        if cxxflags:
            cfg.write(cmake_cache_entry("CMAKE_CXX_FLAGS", cxxflags))

        #######################
        # CUDA
        #######################

        if "+cuda" in spec:
            cfg.write("#------------------{0}\n".format("-" * 60))
            cfg.write("# Cuda\n")
            cfg.write("#------------------{0}\n\n".format("-" * 60))

            cfg.write(cmake_cache_option("MFEM_USE_CUDA", True))

            cudatoolkitdir = spec['cuda'].prefix
            cfg.write(cmake_cache_entry("CUDA_TOOLKIT_ROOT_DIR",
                                        cudatoolkitdir))
            cudacompiler = "${CUDA_TOOLKIT_ROOT_DIR}/bin/nvcc"
            cfg.write(cmake_cache_entry("CMAKE_CUDA_COMPILER",
                                        cudacompiler))

            # JBE: CudaPackage will set this in the environment which overrides
            # anything else - is this related to https://github.com/spack/spack/issues/17823 ??
            if '+mpi' in spec:
                env['CUDAHOSTCXX'] = spec['mpi'].mpicxx

            if spec.satisfies('cuda_arch=none'):
                cfg.write("# No cuda_arch specified in Spack spec, this is likely to fail\n\n")
            else:
                cuda_arch = spec.variants['cuda_arch'].value
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                # CXX flags will be propagated to the host compiler
                cuda_flags = ' '.join([flag, cxxflags])
                cfg.write(cmake_cache_string("CMAKE_CUDA_FLAGS", cuda_flags))
                cfg.write(cmake_cache_string("CMAKE_CUDA_ARCHITECTURES", ' '.join(cuda_arch)))

        else:
            cfg.write(cmake_cache_option("MFEM_USE_CUDA", False))

        xcompiler = ''
        xlinker = '-Wl,'
        #if '+cuda' in spec:
        #    xcompiler = '-Xcompiler='
        #    xlinker = '-Xlinker='

        #cxxflags = [(xcompiler + flag) for flag in cxxflags]

        #if '+cuda' in spec:
        #        cxxflags += [
        #            '-x=cu --expt-extended-lambda -arch=%s' % cuda_arch,
        #            '-ccbin %s' % (spec['mpi'].mpicxx if '+mpi' in spec
        #                           else env['CXX'])]

        #######################
        # MPI
        #######################

        # Determine how to run MPI tests, e.g. when using '--test=root', when
        # Spack is run inside a batch system job.
        mfem_mpiexec    = 'mpirun'
        mfem_mpiexec_np = '-np'
        if 'SLURM_JOBID' in os.environ:
            mfem_mpiexec    = 'srun'
            mfem_mpiexec_np = '-n'
        elif 'LSB_JOBID' in os.environ:
            if 'LLNL_COMPUTE_NODES' in os.environ:
                mfem_mpiexec    = 'lrun'
                mfem_mpiexec_np = '-n'
            else:
                mfem_mpiexec    = 'jsrun'
                mfem_mpiexec_np = '-p'

        cfg.write("#---------------------------------------\n")
        cfg.write("# MPI\n")
        cfg.write("#---------------------------------------\n")
        if '+mpi' in spec:
            cfg.write(cmake_cache_option("MFEM_USE_MPI", True))
        #    cfg.write(cmake_cache_entry("MPI_C_COMPILER", spec['mpi'].mpicc))
        #    cfg.write(cmake_cache_entry("MPI_CXX_COMPILER",
        #                                spec['mpi'].mpicxx))
        #    if os.path.isfile(mfem_mpiexec):
        #        # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
        #        # vs the older versions which expect MPIEXEC
        #        if self.spec["cmake"].satisfies('@3.10:'):
        #            cfg.write(cmake_cache_string("MPIEXEC_EXECUTABLE", mfem_mpiexec))
        #        else:
        #            cfg.write(cmake_cache_string("MPIEXEC", mfem_mpiexec))

        #else:
        #    cfg.write(cmake_cache_option("MFEM_USE_MPI", False))

        # JBE: PREFIX interferes with generation of CUDA link command
        if '+cuda' not in spec:
            cfg.write(cmake_cache_entry("PREFIX", prefix))

        cfg.write(cmake_cache_option("MFEM_USE_MEMALLOC", True))
        cfg.write(cmake_cache_option("MFEM_DEBUG", on_off('+debug')))
        # NOTE: env['CXX'] is the spack c++ compiler wrapper. The real
        # compiler is defined by env['SPACK_CXX'].
        cfg.write(cmake_cache_string("CXX", env['SPACK_CXX']))

        cfg.write(cmake_cache_option("MFEM_USE_LIBUNWIND", on_off('+libunwind')))
        cfg.write(cmake_cache_option(zlib_var, on_off('+zlib')))
        cfg.write(cmake_cache_option("MFEM_USE_METIS", on_off('+metis')))
        cfg.write(cmake_cache_option("MFEM_USE_METIS_5", metis5_str))
        cfg.write(cmake_cache_option("MFEM_THREAD_SAFE", on_off('+threadsafe')))
        cfg.write(cmake_cache_option("MFEM_USE_LAPACK", on_off('+lapack')))
        cfg.write(cmake_cache_option("MFEM_USE_SUPERLU", on_off('+superlu-dist')))
        cfg.write(cmake_cache_option("MFEM_USE_STRUMPACK", on_off('+strumpack')))
        cfg.write(cmake_cache_option("MFEM_USE_SUITESPARSE", on_off('+suite-sparse')))
        cfg.write(cmake_cache_option("MFEM_USE_SUNDIALS", on_off('+sundials')))
        cfg.write(cmake_cache_option("MFEM_USE_PETSC", on_off('+petsc')))
        cfg.write(cmake_cache_option("MFEM_USE_PUMI", on_off('+pumi')))
        cfg.write(cmake_cache_option("MFEM_USE_GSLIB", on_off('+gslib')))
        cfg.write(cmake_cache_option("MFEM_USE_NETCDF", on_off('+netcdf')))
        cfg.write(cmake_cache_option("MFEM_USE_MPFR", on_off('+mpfr')))
        cfg.write(cmake_cache_option("MFEM_USE_GNUTLS", on_off('+gnutls')))
        cfg.write(cmake_cache_option("MFEM_USE_OPENMP", on_off('+openmp')))
        cfg.write(cmake_cache_option("MFEM_USE_CONDUIT", on_off('+conduit')))
        cfg.write(cmake_cache_option("MFEM_USE_OCCA", on_off('+occa')))
        cfg.write(cmake_cache_option("MFEM_USE_RAJA", on_off('+raja')))
        cfg.write(cmake_cache_option("MFEM_USE_AMGX", on_off('+amgx')))
        cfg.write(cmake_cache_option("MFEM_USE_CEED", on_off('+libceed')))
        cfg.write(cmake_cache_option("MFEM_USE_UMPIRE", on_off('+umpire')))

        if '~static' in spec:
            cfg.write(cmake_cache_option("STATIC", False))

        if '+shared' in spec:
            cfg.write(cmake_cache_option("SHARED", True))
            cfg.write(cmake_cache_string("PICFLAG", self.compiler.cxx_pic_flag))

        if '+mpi' in spec:
            hypre_dir = get_spec_path(spec, "hypre")
            cfg.write(cmake_cache_entry("HYPRE_DIR", hypre_dir))

        if '+metis' in spec:
            metis_dir = get_spec_path(spec, "metis")
            cfg.write(cmake_cache_entry("METIS_DIR", metis_dir))

        if '+lapack' in spec:
            lapack = spec['lapack'].libs
            lapack_inc = spec['lapack'].prefix.include
            lapack_lib = ld_flags_from_library_list(lapack)
            cfg.write(cmake_cache_string("LAPACK_LIBRARIES",lapack_lib))
            cfg.write(cmake_cache_string("LAPACK_INCLUDE_DIRS",lapack_inc))

            blas = spec['blas'].libs
            blas_inc = spec['blas'].prefix.include
            blas_lib = ld_flags_from_library_list(blas)
            cfg.write(cmake_cache_string("BLAS_LIBRARIES",blas_lib))
            cfg.write(cmake_cache_string("BLAS_INCLUDE_DIRS",blas_inc))

            # Parmetis is reguired by superlu-dist.
            # The MFEM way is to provide superlu with it's parmetis dependency
            # location. A better way would be to have superlu autonomous for
            # this, but requires changes in MFEM CMake build-system.
        if '+superlu-dist' in spec:
            parmetis_dir = get_spec_path(spec, "parmetis")
            cfg.write(cmake_cache_entry("ParMETIS_DIR", parmetis_dir))

            #TODO (bernede1@llnl.gov): what about PARMETIS_REQUIRED_PACKAGES
            # see MFEM config/defaults.cmake

        if '+superlu-dist' in spec:
            superludist_dir = get_spec_path(spec, "superlu-dist")
            cfg.write(cmake_cache_entry("SuperLUDist_DIR", superludist_dir))

            #TODO (bernede1@llnl.gov): what about SUPERLUDIST_REQUIRED_PACKAGES
            # see MFEM config/defaults.cmake

        if '+strumpack' in spec:
            strumpack_dir = get_spec_path(spec, "strumpack")
            cfg.write(cmake_cache_entry("STRUMPACK_DIR", strumpack_dir))

            #TODO (bernede1@llnl.gov): what about STRUMPACK_REQUIRED_PACKAGES
            # see MFEM config/defaults.cmake

        if '+suite-sparse' in spec:
            suitesparse_dir = get_spec_path(spec, "suitesparse")
            cfg.write(cmake_cache_entry("SuiteSparse_DIR", suitesparse_dir))

        if '+sundials' in spec:
            sundials_dir = get_spec_path(spec, "sundials")
            cfg.write(cmake_cache_entry("SUNDIALS_DIR", sundials_dir))

        if '+petsc' in spec:
            petsc_dir = get_spec_path(spec, "petsc")
            cfg.write(cmake_cache_entry("PETSC_DIR", petsc_dir))
            cfg.write(cmake_cache_entry("PETSC_ARCH", ""))

            #TODO (bernede1@llnl.gov): what about PETSC_REQUIRED_PACKAGES
            # see MFEM config/defaults.cmake

            #petsc = spec['petsc']
            #if '+shared' in petsc:
            #    petsc_opt = petsc.headers.cpp_flags
            #    petsc_lib = ld_flags_from_library_list(petsc.libs)

            #    cfg.write(cmake_cache_string("PETSC_OPT", petsc_opt))
            #    cfg.write(cmake_cache_string("PETSC_LIB", petsc_lib))
            #else:
            #    cfg.write(cmake_cache_string("PETSC_DIR", petsc.prefix))

        if '+pumi' in spec:
            pumi_dir = get_spec_path(spec, "pumi")
            cfg.write(cmake_cache_entry("PUMI_DIR", pumi_dir))

        if '+gslib' in spec:
            gslib_dir = get_spec_path(spec, "gslib")
            cfg.write(cmake_cache_entry("GSLIB_DIR", gslib_dir))

        if '+netcdf' in spec:
            netcdf_dir = get_spec_path(spec, "netcdf-c")
            cfg.write(cmake_cache_entry("NETCDF_DIR", netcdf_dir))

            hdf5_dir = get_spec_path(spec, "hdf5")
            cfg.write(cmake_cache_entry("HDF5_DIR", hdf5_dir))

        if '+zlib' in spec:
            if "@:3.3.2" in spec:
                zlib_dir = spec['zlib'].prefix
                cfg.write(cmake_cache_entry("ZLIB_DIR", zlib_dir))
            else:
                zlib_opt = '-I%s' % spec['zlib'].prefix.include
                zlib_lib = ld_flags_from_library_list(spec['zlib'].libs)

                cfg.write(cmake_cache_string("ZLIB_OPT", zlib_opt))
                cfg.write(cmake_cache_string("ZLIB_LIB", zlib_lib))

        if '+mpfr' in spec:
            mpfr_dir = get_spec_path(spec, "mpfr")
            cfg.write(cmake_cache_entry("MPFR_DIR", mpfr_dir))

        if '+gnutls' in spec:
            gnutls_dir = get_spec_path(spec, "gnutls")
            cfg.write(cmake_cache_entry("GNUTLS_DIR", gnutls_dir))

        if '+libunwind' in spec:
            libunwind_dir = get_spec_path(spec, "libunwind")
            cfg.write(cmake_cache_entry("LIBUNWIND_DIR", libunwind_dir))

        if '+openmp' in spec:
            cfg.write(cmake_cache_string("OPENMP_OPT", self.compiler.openmp_flag))

        if '+cuda' in spec:
            cuda_cxx = join_path(spec['cuda'].prefix, 'bin', 'nvcc')

            cfg.write(cmake_cache_string("CUDA_CXX", cuda_cxx))
            cfg.write(cmake_cache_string("CUDA_ARCH", 'sm_{0}'.format(cuda_arch[0])))

        if '+occa' in spec:
            occa_dir = get_spec_path(spec, "occa")
            cfg.write(cmake_cache_entry("OCCA_DIR", occa_dir))

        if '+raja' in spec:
            raja_dir = get_spec_path(spec, "raja")
            cfg.write(cmake_cache_entry("RAJA_DIR", raja_dir))

        if '+amgx' in spec:
            amgx_dir = get_spec_path(spec, "amgx")
            cfg.write(cmake_cache_string("AMGX_DIR", amgx_dir))

        if '+libceed' in spec:
            ceed_dir = get_spec_path(spec, "libceed")
            cfg.write(cmake_cache_entry("CEED_DIR", ceed_dir))

        if '+umpire' in spec:
            umpire_dir = get_spec_path(spec, "umpire")
            cfg.write(cmake_cache_entry("UMPIRE_DIR", umpire_dir))

        timer_ids = {'std': '0', 'posix': '2', 'mac': '4', 'mpi': '6'}
        timer = spec.variants['timer'].value
        if timer != 'auto':
            cfg.write(cmake_cache_string("MFEM_TIMER_TYPE",timer_ids[timer]))

        if '+conduit' in spec:
            conduit_dir = get_spec_path(spec, "conduit")
            cfg.write(cmake_cache_entry("CONDUIT_DIR", conduit_dir))

        #######################
        # Close and save
        #######################
        cfg.write("\n")
        cfg.close()

    def cmake_args(self):
        host_config_path = self._get_host_config_path(self.spec)

        options = []
        options.extend(['-DVERBOSE=1'])
        options.extend(['-C', host_config_path])
        return options

#    def build(self, spec, prefix):
#        make('lib')
#
#    @run_after('build')
#    def check_or_test(self):
#        # Running 'make check' or 'make test' may fail if MFEM_MPIEXEC or
#        # MFEM_MPIEXEC_NP are not set appropriately.
#        if not self.run_tests:
#            # check we can build ex1 (~mpi) or ex1p (+mpi).
#            make('-C', 'examples', 'ex1p' if ('+mpi' in self.spec) else 'ex1',
#                 parallel=False)
#            # make('check', parallel=False)
#        else:
#            make('all')
#            make('test', parallel=False)
#
#    def install(self, spec, prefix):
#        make('install', parallel=False)
#
#        # TODO: The way the examples and miniapps are being installed is not
#        # perfect. For example, the makefiles do not work.
#
#        install_em = ('+examples' in spec) or ('+miniapps' in spec)
#        if install_em and ('+shared' in spec):
#            make('examples/clean', 'miniapps/clean')
#            # This is a hack to get the examples and miniapps to link with the
#            # installed shared mfem library:
#            with working_dir('config'):
#                os.rename('config.mk', 'config.mk.orig')
#                copy(str(self.config_mk), 'config.mk')
#                shutil.copystat('config.mk.orig', 'config.mk')
#
#        prefix_share = join_path(prefix, 'share', 'mfem')
#
#        if '+examples' in spec:
#            make('examples')
#            install_tree('examples', join_path(prefix_share, 'examples'))
#
#        if '+miniapps' in spec:
#            make('miniapps')
#            install_tree('miniapps', join_path(prefix_share, 'miniapps'))
#
#        if install_em:
#            install_tree('data', join_path(prefix_share, 'data'))

    @when('@4.1.0')
    def patch(self):
        # Remove the byte order mark since it messes with some compilers
        files_with_bom = [
            'fem/gslib.hpp', 'fem/gslib.cpp', 'linalg/hiop.hpp',
            'miniapps/gslib/field-diff.cpp', 'miniapps/gslib/findpts.cpp',
            'miniapps/gslib/pfindpts.cpp']
        bom = '\xef\xbb\xbf' if sys.version_info < (3,) else u'\ufeff'
        for f in files_with_bom:
            filter_file(bom, '', f)

    @property
    def suitesparse_components(self):
        """Return the SuiteSparse components needed by MFEM."""
        ss_comps = 'umfpack,cholmod,colamd,amd,camd,ccolamd,suitesparseconfig'
        if self.spec.satisfies('@3.2:'):
            ss_comps = 'klu,btf,' + ss_comps
        return ss_comps

    @property
    def sundials_components(self):
        """Return the SUNDIALS components needed by MFEM."""
        spec = self.spec
        sun_comps = 'arkode,cvodes,nvecserial,kinsol'
        if '+mpi' in spec:
            if spec.satisfies('@4.2:'):
                sun_comps += ',nvecparallel,nvecmpiplusx'
            else:
                sun_comps += ',nvecparhyp,nvecparallel'
        if '+cuda' in spec and '+cuda' in spec['sundials']:
            sun_comps += ',nveccuda'
        return sun_comps

    @property
    def headers(self):
        """Export the main mfem header, mfem.hpp.
        """
        hdrs = HeaderList(find(self.prefix.include, 'mfem.hpp',
                               recursive=False))
        return hdrs or None

    @property
    def libs(self):
        """Export the mfem library file.
        """
        libs = find_libraries('libmfem', root=self.prefix.lib,
                              shared=('+shared' in self.spec), recursive=False)
        return libs or None

    @property
    def config_mk(self):
        """Export the location of the config.mk file.
           This property can be accessed using spec['mfem'].package.config_mk
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, 'config.mk')
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, 'config.mk', recursive=True))

    @property
    def test_mk(self):
        """Export the location of the test.mk file.
           This property can be accessed using spec['mfem'].package.test_mk.
           In version 3.3.2 and newer, the location of test.mk is also defined
           inside config.mk, variable MFEM_TEST_MK.
        """
        dirs = [self.prefix, self.prefix.share.mfem]
        for d in dirs:
            f = join_path(d, 'test.mk')
            if os.access(f, os.R_OK):
                return FileList(f)
        return FileList(find(self.prefix, 'test.mk', recursive=True))
