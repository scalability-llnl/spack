# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Occa(Package):
    """OCCA is an open-source (MIT license) library used to program current
       multi-core/many-core architectures. Devices (such as CPUs, GPUs,
       Intel's Xeon Phi, FPGAs, etc) are abstracted using an offload-model
       for application development and programming for the devices is done
       through a C-based (OKL) or Fortran-based kernel language (OFL).
       OCCA gives developers the ability to target devices at run-time by
       using run-time compilation for device kernels.
    """

    homepage = "http://libocca.org"
    git      = 'https://github.com/libocca/occa.git'

    maintainers = ['v-dobrev', 'dmed256']

    version('develop')
    version('1.1.0', tag='v1.1.0')
    version('1.0.9', tag='v1.0.9')
    version('1.0.8', tag='v1.0.8')
    version('1.0.0-alpha.5', tag='v1.0.0-alpha.5')
    version('0.2.0', tag='v0.2.0')
    version('0.1.0', tag='v0.1.0')

    variant('cuda',
            default=True,
            description='Activates support for CUDA')
    variant('openmp',
            default=True,
            description='Activates support for OpenMP')
    variant('opencl',
            default=True,
            description='Activates support for OpenCL')

    depends_on('cuda', when='+cuda')

    conflicts('%gcc@6:', when='^cuda@:8')
    conflicts('%gcc@7:', when='^cuda@:9')

    def install(self, spec, prefix):
        # The build environment is set by the 'setup_build_environment' method.
        # Copy the source to the installation directory and build OCCA there.
        install_tree('.', prefix)
        make('-C', prefix)

        if self.run_tests:
            make('-C', prefix, 'test', parallel=False)

    def _setup_runtime_flags(self, s_env):
        spec = self.spec
        s_env.set('OCCA_DIR', self.prefix)
        s_env.set('OCCA_CXX', self.compiler.cxx)

        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            # Run-time compiler flags:
            s_env.set('OCCA_CXXFLAGS', ' '.join(cxxflags))

        if '+cuda' in spec:
            cuda_dir = spec['cuda'].prefix
            # Run-time CUDA compiler:
            s_env.set('OCCA_CUDA_COMPILER',
                      join_path(cuda_dir, 'bin', 'nvcc'))

    def setup_build_environment(self, env):
        spec = self.spec
        # The environment variable CXX is automatically set to the Spack
        # compiler wrapper.

        # The cxxflags, if specified, will be set by the Spack compiler wrapper
        # while the environment variable CXXFLAGS will remain undefined.
        # We define CXXFLAGS in the environment to tell OCCA to use the user
        # specified flags instead of its defaults. This way the compiler will
        # get the cxxflags twice - once from the Spack compiler wrapper and
        # second time from OCCA - however, only the second one will be seen in
        # the verbose output, so we keep both.
        cxxflags = spec.compiler_flags['cxxflags']
        if cxxflags:
            env.set('CXXFLAGS', ' '.join(cxxflags))

        # For the cuda, openmp, and opencl variants, set the environment
        # variable OCCA_{CUDA,OPENMP,OPENCL}_ENABLED only if the variant is
        # disabled. Otherwise, let OCCA autodetect what is available.

        if '+cuda' in spec:
            cuda_dir = spec['cuda'].prefix
            cuda_libs_list = ['libcuda', 'libcudart', 'libOpenCL']
            cuda_libs = find_libraries(cuda_libs_list,
                                       cuda_dir,
                                       shared=True,
                                       recursive=True)
            env.set('OCCA_INCLUDE_PATH', cuda_dir.include)
            env.set('OCCA_LIBRARY_PATH', ':'.join(cuda_libs.directories))
        else:
            env.set('OCCA_CUDA_ENABLED', '0')

        # Disable hip autodetection for now since it fails on some machines.
        env.set('OCCA_HIP_ENABLED', '0')

        if '~opencl' in spec:
            env.set('OCCA_OPENCL_ENABLED', '0')

        # Setup run-time environment for testing.
        env.set('OCCA_VERBOSE', '1')
        self._setup_runtime_flags(env)

    def setup_run_environment(self, env):
        # The 'env' is included in the Spack generated module files.
        self._setup_runtime_flags(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Export OCCA_* variables for everyone using this package from within
        # Spack.
        self._setup_runtime_flags(env)
