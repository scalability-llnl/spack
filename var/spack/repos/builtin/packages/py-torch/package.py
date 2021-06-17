# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class PyTorch(PythonPackage, CudaPackage):
    """Tensors and Dynamic neural networks in Python
    with strong GPU acceleration."""

    homepage = "https://pytorch.org/"
    git      = "https://github.com/pytorch/pytorch.git"

    maintainers = ['adamjstewart']

    # Exact set of modules is version- and variant-specific, just attempt to import the
    # core libraries to ensure that the package was successfully installed.
    import_modules = ['torch', 'torch.autograd', 'torch.nn', 'torch.utils']

    version('master', branch='master', submodules=True)
    version('1.9.0', tag='v1.9.0', submodules=True)
    version('1.8.1', tag='v1.8.1', submodules=True)
    version('1.8.0', tag='v1.8.0', submodules=True)
    version('1.7.1', tag='v1.7.1', submodules=True)
    version('1.7.0', tag='v1.7.0', submodules=True)
    version('1.6.0', tag='v1.6.0', submodules=True)
    version('1.5.1', tag='v1.5.1', submodules=True)
    version('1.5.0', tag='v1.5.0', submodules=True)
    version('1.4.1', tag='v1.4.1', submodules=True)
    version('1.4.0', tag='v1.4.0', submodules=True,
            submodules_delete=['third_party/fbgemm'])
    version('1.3.1', tag='v1.3.1', submodules=True)
    version('1.3.0', tag='v1.3.0', submodules=True)
    version('1.2.0', tag='v1.2.0', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)
    version('1.0.1', tag='v1.0.1', submodules=True)
    version('1.0.0', tag='v1.0.0', submodules=True)
    version('0.4.1', tag='v0.4.1', submodules=True,
            submodules_delete=['third_party/nervanagpu'])
    version('0.4.0', tag='v0.4.0', submodules=True)
    version('0.3.1', tag='v0.3.1', submodules=True)

    is_darwin = sys.platform == 'darwin'

    # All options are defined in CMakeLists.txt.
    # Some are listed in setup.py, but not all.
    variant('caffe2', default=True, description='Build Caffe2')
    variant('cuda', default=not is_darwin, description='Use CUDA')
    variant('rocm', default=not is_darwin, description='Use ROCm')
    variant('cudnn', default=not is_darwin, description='Use cuDNN')
    variant('fbgemm', default=True, description='Use FBGEMM (quantized 8-bit server operators)')
    variant('kineto', default=True, description='Use Kineto profiling library')
    variant('magma', default=not is_darwin, description='Use MAGMA')
    variant('metal', default=is_darwin, description='Use Metal for Caffe2 iOS build')
    variant('nccl', default=not is_darwin, description='Use NCCL')
    variant('nnpack', default=True, description='Use NNPACK')
    variant('numa', default=not is_darwin, description='Use NUMA')
    variant('numpy', default=True, description='Use NumPy')
    variant('openmp', default=True, description='Use OpenMP for parallel code')
    variant('qnnpack', default=True, description='Use QNNPACK (quantized 8-bit operators)')
    variant('valgrind', default=not is_darwin, description='Use Valgrind')
    variant('xnnpack', default=True, description='Use XNNPACK')
    variant('mkldnn', default=True, description='Use MKLDNN')
    variant('distributed', default=not is_darwin, description='Use distributed')
    variant('mpi', default=not is_darwin, description='Use MPI for Caffe2')
    variant('gloo', default=not is_darwin, description='Use Gloo')
    variant('tensorpipe', default=not is_darwin, description='Use TensorPipe')
    variant('onnx_ml', default=True, description='Enable traditional ONNX ML API')

    conflicts('+cudnn', when='~cuda')
    conflicts('+nccl', when='~cuda~rocm')
    conflicts('+nccl', when='platform=darwin')
    conflicts('+numa', when='platform=darwin', msg='Only available on Linux')
    conflicts('+valgrind', when='platform=darwin', msg='Only available on Linux')
    conflicts('+mpi', when='~distributed')
    conflicts('+gloo', when='~distributed')
    conflicts('+tensorpipe', when='~distributed')
    conflicts('+magma', when='@:1.8.999')
    conflicts('+kineto', when='@:1.7.999')
    conflicts('+valgrind', when='@:1.7.999')
    conflicts('+caffe2', when='@:1.6.999')
    conflicts('+tensorpipe', when='@:1.5.999')
    conflicts('+xnnpack', when='@:1.4.999')
    conflicts('+onnx_ml', when='@:1.4.999')
    conflicts('+rocm', when='@:0.4.999')
    conflicts('+cudnn', when='@:0.4.999')
    conflicts('+fbgemm', when='@:0.4.999')
    conflicts('+qnnpack', when='@:0.4.999')
    conflicts('+mkldnn', when='@:0.4.999')

    conflicts('cuda_arch=none', when='+cuda',
              msg='Must specify CUDA compute capabilities of your GPU, see '
              'https://developer.nvidia.com/cuda-gpus')

    # Required dependencies
    depends_on('cmake@3.5:', type='build')
    # Use Ninja generator to speed up build times, automatically used if found
    depends_on('ninja@1.5:', type='build')
    # See python_min_version in setup.py
    depends_on('python@3.6.2:', when='@1.7.1:', type=('build', 'link', 'run'))
    depends_on('python@3.6.1:', when='@1.6:', type=('build', 'link', 'run'))
    depends_on('python@3.5:', when='@1.5:', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-future', when='@1.5:', type=('build', 'run'))
    depends_on('py-future', when='@1.1: ^python@:2', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-typing', when='@0.4: ^python@:3.4', type=('build', 'run'))
    depends_on('py-typing-extensions', when='@1.7:', type=('build', 'run'))
    depends_on('py-pybind11', when='@0.4:', type=('build', 'link', 'run'))
    depends_on('py-dataclasses', when='@1.7: ^python@3.6.0:3.6.999', type=('build', 'run'))
    depends_on('py-tqdm', type='run')
    depends_on('blas')
    depends_on('lapack')
    depends_on('protobuf', when='@0.4:')
    depends_on('py-protobuf', when='@0.4:', type=('build', 'run'))
    depends_on('eigen', when='@0.4:')

    # Optional dependencies
    depends_on('cuda@7.5:', when='+cuda', type=('build', 'link', 'run'))
    depends_on('cuda@9:', when='@1.1:+cuda', type=('build', 'link', 'run'))
    depends_on('cudnn@6:', when='+cudnn')
    depends_on('cudnn@7:', when='@1.1:+cudnn')
    depends_on('fbgemm@master', when='@master+fbgemm')
    depends_on('fbgemm@2021-05-10', when='@1.9.0:1.9.999+fbgemm')
    depends_on('fbgemm@2020-11-13', when='@1.8.0:1.8.999+fbgemm')
    depends_on('fbgemm@2020-09-14', when='@1.7.0:1.7.999+fbgemm')
    depends_on('fbgemm@2020-05-31', when='@1.6.0:1.6.999+fbgemm')
    depends_on('fbgemm@2020-05-21', when='@1.5.1+fbgemm')
    depends_on('fbgemm@2020-03-22', when='@1.5.0+fbgemm')
    depends_on('fbgemm@2019-11-20', when='@1.4.0:1.4.999+fbgemm')
    depends_on('fbgemm@2019-09-26', when='@1.3.0:1.3.999+fbgemm')
    depends_on('fbgemm@2019-07-22', when='@1.2.0:1.2.999+fbgemm')
    depends_on('fbgemm@2019-04-18', when='@1.1.0:1.1.999+fbgemm')
    depends_on('fbgemm@2019-01-23', when='@1.0.1+fbgemm')
    depends_on('fbgemm@2018-12-04', when='@1.0.0+fbgemm')
    depends_on('kineto@master', when='@master+kineto')
    depends_on('kineto@2021-05-12', when='@1.9.0+kineto')
    depends_on('kineto@2021-03-16', when='@1.8.1+kineto')
    depends_on('kineto@2021-02-04', when='@1.8.0+kineto')
    depends_on('magma', when='+magma')
    depends_on('nccl', when='+nccl')
    depends_on('nnpack@master', when='@master+nnpack')
    depends_on('nnpack@2020-12-21', when='@1.8.0:1.9.999+nnpack')
    depends_on('nnpack@2019-10-07', when='@1.4.0:1.7.999+nnpack')
    depends_on('nnpack@2019-03-23', when='@1.1.0:1.3.999+nnpack')
    depends_on('nnpack@2018-09-03', when='@1.0.0:1.0.999+nnpack')
    depends_on('nnpack@2018-05-21', when='@0.4.1+nnpack')
    depends_on('nnpack@2018-04-05', when='@:0.4.0+nnpack')
    depends_on('numactl', when='+numa')
    depends_on('py-numpy', when='+numpy', type=('build', 'run'))
    depends_on('llvm-openmp', when='%apple-clang +openmp')
    depends_on('qnnpack@master', when='@master+qnnpack')
    depends_on('qnnpack@2019-08-28', when='@1.3.0:1.9.999+qnnpack')
    depends_on('qnnpack@2018-12-27', when='@1.2.0:1.2.999+qnnpack')
    depends_on('qnnpack@2018-12-04', when='@1.0.0:1.1.999+qnnpack')
    depends_on('valgrind', when='+valgrind')
    depends_on('xnnpack@master', when='@master+xnnpack')
    depends_on('xnnpack@2021-02-22', when='@1.8.0:1.9.999+xnnpack')
    depends_on('xnnpack@2020-03-23', when='@1.6.0:1.7.999+xnnpack')
    depends_on('xnnpack@2020-02-24', when='@1.5.0:1.5.999+xnnpack')
    depends_on('onednn', when='+mkldnn')
    depends_on('mpi', when='+mpi')
    depends_on('gloo@master', when='@master+gloo')
    depends_on('gloo@2021-05-04', when='@1.9.0:1.9.999+gloo')
    depends_on('gloo@2020-09-18', when='@1.7.0:1.8.999+gloo')
    depends_on('gloo@2020-03-17', when='@1.5.0:1.6.999+gloo')
    depends_on('gloo@2019-11-05', when='@1.4.0:1.4.999+gloo')
    depends_on('gloo@2019-09-29', when='@1.3.0:1.3.999+gloo')
    depends_on('gloo@2019-06-19', when='@1.2.0:1.2.999+gloo')
    depends_on('gloo@2019-02-01', when='@1.0.1:1.1.999+gloo')
    depends_on('gloo@2018-11-20', when='@1.0.0+gloo')
    depends_on('gloo@2018-05-29', when='@0.4.1+gloo')
    depends_on('gloo@2018-04-06', when='@:0.4.0+gloo')
    depends_on('tensorpipe@master', when='@master+tensorpipe')
    depends_on('tensorpipe@2021-05-13', when='@1.9.0:1.9.999+tensorpipe')
    depends_on('tensorpipe@2021-03-04', when='@1.8.1+tensorpipe')
    depends_on('tensorpipe@2021-02-09', when='@1.8.0+tensorpipe')
    depends_on('tensorpipe@2020-09-28', when='@1.7.0:1.7.999+tensorpipe')
    depends_on('tensorpipe@2020-06-26', when='@1.6.0:1.6.999+tensorpipe')

    # Test dependencies
    depends_on('py-hypothesis', type='test')
    depends_on('py-six', type='test')
    depends_on('py-psutil', type='test')

    # Fixes build on older systems with glibc <2.12
    patch('https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/55063.patch',
          sha256='e17eaa42f5d7c18bf0d7c37d7b0910127a01ad53fdce3e226a92893356a70395',
          when='@1.1.0:1.8.1')

    # https://github.com/pytorch/pytorch/pull/35607
    # https://github.com/pytorch/pytorch/pull/37865
    # Fixes CMake configuration error when XNNPACK is disabled
    patch('xnnpack.patch', when='@1.5.0:1.5.999')

    # Fixes build error when ROCm is enabled for pytorch-1.5 release
    patch('rocm.patch', when='@1.5.0:1.5.999+rocm')

    # https://github.com/pytorch/pytorch/pull/37086
    # Fixes compilation with Clang 9.0.0 and Apple Clang 11.0.3
    patch('https://github.com/pytorch/pytorch/commit/e921cd222a8fbeabf5a3e74e83e0d8dfb01aa8b5.patch',
          sha256='17561b16cd2db22f10c0fe1fdcb428aecb0ac3964ba022a41343a6bb8cba7049',
          when='@1.1:1.5')

    # Fix for 'FindOpenMP.cmake'
    # to detect openmp settings used by Fujitsu compiler.
    patch('detect_omp_of_fujitsu_compiler.patch', when='%fj')

    # Both build and install run cmake/make/make install
    # Only run once to speed up build times
    phases = ['install']

    @property
    def libs(self):
        root = join_path(
            self.prefix, self.spec['python'].package.site_packages_dir,
            'torch', 'lib')
        return find_libraries('libtorch', root)

    @property
    def headers(self):
        root = join_path(
            self.prefix, self.spec['python'].package.site_packages_dir,
            'torch', 'include')
        headers = find_all_headers(root)
        headers.directories = [root]
        return headers

    @when('@1.5.0:')
    def patch(self):
        # https://github.com/pytorch/pytorch/issues/52208
        filter_file('torch_global_deps PROPERTIES LINKER_LANGUAGE C',
                    'torch_global_deps PROPERTIES LINKER_LANGUAGE CXX',
                    'caffe2/CMakeLists.txt')

    def setup_build_environment(self, env):
        """Set environment variables used to control the build.

        PyTorch's ``setup.py`` is a thin wrapper around ``cmake``.
        In ``tools/setup_helpers/cmake.py``, you can see that all
        environment variables that start with ``BUILD_``, ``USE_``,
        or ``CMAKE_``, plus a few more explicitly specified variable
        names, are passed directly to the ``cmake`` call. Therefore,
        most flags defined in ``CMakeLists.txt`` can be specified as
        environment variables.
        """
        def enable_or_disable(variant, keyword='USE', newer=False):
            """Set environment variable to enable or disable support for a
            particular variant.

            Parameters:
                variant (str): the variant to check
                keyword (str): the prefix to use for enabling/disabling
                newer (bool): newer variants that never used NO_*
            """
            var = variant.upper()

            # Version 1.1.0 switched from NO_* to USE_* or BUILD_*
            # But some newer variants have always used USE_* or BUILD_*
            if self.spec.satisfies('@1.1:') or newer:
                if '+' + variant in self.spec:
                    env.set(keyword + '_' + var, 'ON')
                else:
                    env.set(keyword + '_' + var, 'OFF')
            else:
                if '+' + variant in self.spec:
                    env.unset('NO_' + var)
                else:
                    env.set('NO_' + var, 'ON')

        # Build in parallel to speed up build times
        env.set('MAX_JOBS', make_jobs)

        # Spack logs have trouble handling colored output
        env.set('COLORIZE_OUTPUT', 'OFF')

        enable_or_disable('caffe2', keyword='BUILD')

        enable_or_disable('cuda')
        if '+cuda' in self.spec:
            # cmake/public/cuda.cmake
            # cmake/Modules_CUDA_fix/upstream/FindCUDA.cmake
            env.set('CUDA_HOME', self.spec['cuda'].prefix)
            torch_cuda_arch = ';'.join('{0:.1f}'.format(float(i) / 10.0) for i
                                       in
                                       self.spec.variants['cuda_arch'].value)
            env.set('TORCH_CUDA_ARCH_LIST', torch_cuda_arch)

        enable_or_disable('rocm')

        enable_or_disable('cudnn')
        if '+cudnn' in self.spec:
            # cmake/Modules_CUDA_fix/FindCUDNN.cmake
            env.set('CUDNN_ROOT', self.spec['cudnn'].prefix)
            env.set('CUDNN_INCLUDE_DIR', self.spec['cudnn'].prefix.include)
            env.set('CUDNN_LIBRARY', self.spec['cudnn'].libs[0])

        enable_or_disable('fbgemm')
        enable_or_disable('kineto')
        enable_or_disable('magma')
        enable_or_disable('metal')

        enable_or_disable('nccl')
        if '+nccl' in self.spec:
            env.set('NCCL_ROOT', self.spec['nccl'].prefix)
            env.set('NCCL_LIB_DIR', self.spec['nccl'].libs.directories[0])
            env.set('NCCL_INCLUDE_DIR', self.spec['nccl'].prefix.include)

        # cmake/External/nnpack.cmake
        enable_or_disable('nnpack')

        enable_or_disable('numa')
        if '+numa' in self.spec:
            # cmake/Modules/FindNuma.cmake
            env.set('NUMA_ROOT_DIR', self.spec['numactl'].prefix)

        # cmake/Modules/FindNumPy.cmake
        enable_or_disable('numpy')
        # cmake/Modules/FindOpenMP.cmake
        enable_or_disable('openmp', newer=True)
        enable_or_disable('qnnpack')
        enable_or_disable('valgrind')
        enable_or_disable('xnnpack')

        enable_or_disable('mkldnn')
        if '+mkldnn' in self.spec:
            # cmake/public/mkldnn.cmake
            # cmake/Modules/FindMKLDNN.cmake
            env.set('MKLDNN_HOME', self.spec['onednn'].prefix)

        enable_or_disable('distributed')
        enable_or_disable('mpi')
        # cmake/Modules/FindGloo.cmake
        enable_or_disable('gloo', newer=True)
        enable_or_disable('tensorpipe')
        enable_or_disable('onnx_ml')

        if not self.spec.satisfies('@master'):
            env.set('PYTORCH_BUILD_VERSION', self.version)
            env.set('PYTORCH_BUILD_NUMBER', 0)

        # BLAS to be used by Caffe2
        if '^mkl' in self.spec:
            env.set('BLAS', 'MKL')
        elif '^atlas' in self.spec:
            env.set('BLAS', 'ATLAS')
        elif '^openblas' in self.spec:
            env.set('BLAS', 'OpenBLAS')
        elif '^veclibfort' in self.spec:
            env.set('BLAS', 'vecLib')
        elif '^libflame' in self.spec:
            env.set('BLAS', 'FLAME')
        elif '^eigen' in self.spec:
            env.set('BLAS', 'Eigen')

        # Don't use vendored third-party libraries
        env.set('BUILD_CUSTOM_PROTOBUF', 'OFF')
        env.set('USE_PYTORCH_QNNPACK', 'OFF')
        env.set('USE_SYSTEM_NCCL', 'ON')
        env.set('USE_SYSTEM_EIGEN_INSTALL', 'ON')
        env.set('USE_SYSTEM_LIBS', 'ON')
        env.set('USE_SYSTEM_CPUINFO', 'ON')
        env.set('USE_SYSTEM_SLEEF', 'ON')
        env.set('USE_SYSTEM_GLOO', 'ON')
        env.set('USE_SYSTEM_FP16', 'ON')
        env.set('USE_SYSTEM_PYBIND11', 'ON')
        env.set('pybind11_DIR', self.spec['py-pybind11'].prefix)
        env.set('pybind11_INCLUDE_DIR',
                self.spec['py-pybind11'].prefix.include)
        env.set('USE_SYSTEM_PTHREADPOOL', 'ON')
        env.set('USE_SYSTEM_PSIMD', 'ON')
        env.set('USE_SYSTEM_FXDIV', 'ON')
        env.set('USE_SYSTEM_BENCHMARK', 'ON')
        env.set('USE_SYSTEM_ONNX', 'ON')
        env.set('USE_SYSTEM_XNNPACK', 'ON')

    @run_before('install')
    def build_amd(self):
        if '+rocm' in self.spec:
            python(os.path.join('tools', 'amd_build', 'build_amd.py'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('test'):
            python('run_test.py')

    # Tests need to be re-added since `phases` was overridden
    run_after('install')(
        PythonPackage._run_default_install_time_test_callbacks)
    run_after('install')(PythonPackage.sanity_check_prefix)
