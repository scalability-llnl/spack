# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Mxnet(CMakePackage, CudaPackage):
    """MXNet is a deep learning framework
    designed for both efficiency and flexibility."""

    homepage = "https://mxnet.apache.org"
    url      = "https://archive.apache.org/dist/incubator/mxnet/1.7.0/apache-mxnet-src-1.7.0-incubating.tar.gz"
    list_url = "https://mxnet.apache.org/get_started/download"
    git      = "https://github.com/apache/incubator-mxnet.git"

    maintainers = ['adamjstewart']
    import_modules = [
        'mxnet', 'mxnet.numpy_extension', 'mxnet.optimizer', 'mxnet.module',
        'mxnet.io', 'mxnet.cython', 'mxnet.ndarray', 'mxnet.gluon',
        'mxnet.symbol', 'mxnet._cy3', 'mxnet.contrib', 'mxnet.numpy',
        'mxnet._ffi', 'mxnet.image', 'mxnet.kvstore', 'mxnet.notebook',
        'mxnet._ctypes', 'mxnet.rnn', 'mxnet.ndarray.numpy_extension',
        'mxnet.ndarray.numpy', 'mxnet.gluon.nn', 'mxnet.gluon.model_zoo',
        'mxnet.gluon.contrib', 'mxnet.gluon.data', 'mxnet.gluon.rnn',
        'mxnet.gluon.model_zoo.vision', 'mxnet.gluon.contrib.nn',
        'mxnet.gluon.contrib.estimator', 'mxnet.gluon.contrib.cnn',
        'mxnet.gluon.contrib.data', 'mxnet.gluon.contrib.rnn',
        'mxnet.gluon.data.vision', 'mxnet.symbol.numpy_extension',
        'mxnet.symbol.numpy', 'mxnet.contrib.onnx',
        'mxnet.contrib.svrg_optimization', 'mxnet.contrib.amp',
        'mxnet.contrib.text', 'mxnet.contrib.onnx.mx2onnx',
        'mxnet.contrib.onnx.onnx2mx', 'mxnet.contrib.amp.lists',
        'mxnet._ffi._cy3', 'mxnet._ffi._ctypes'
    ]

    version('master', branch='master')
    version('1.master', branch='v1.x')
    version('1.7.0', sha256='1d20c9be7d16ccb4e830e9ee3406796efaf96b0d93414d676337b64bc59ced18')
    version('1.6.0', sha256='01eb06069c90f33469c7354946261b0a94824bbaf819fd5d5a7318e8ee596def')
    version('1.3.0', sha256='c00d6fbb2947144ce36c835308e603f002c1eb90a9f4c5a62f4d398154eed4d2', deprecated=True)

    variant('build_type', default='Distribution',
            description='CMake build type',
            values=('Distribution', 'Debug', 'Release',
                    'RelWithDebInfo', 'MinSizeRel'))
    variant('cuda', default=True, description='Enable CUDA support')
    variant('cudnn', default=True, description='Build with cudnn support')
    variant('nccl', default=False, description='Use NVidia NCCL with CUDA')
    variant('opencv', default=True, description='Enable OpenCV support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('lapack', default=True, description='Build with lapack support')
    variant('mkldnn', default=False, description='Build with MKL-DNN support')
    variant('python', default=True, description='Install python bindings')

    depends_on('cmake@3.13:', type='build')
    depends_on('ninja', type='build')
    depends_on('pkgconfig', when='@1.6.0', type='build')
    depends_on('blas')
    depends_on('cudnn', when='+cudnn')
    depends_on('nccl', when='+nccl')
    depends_on('opencv+core+highgui+imgproc+imgcodecs', when='+opencv')
    depends_on('lapack', when='+lapack')
    depends_on('onednn', when='+mkldnn')

    # python/setup.py
    extends('python', when='+python')
    depends_on('python@2.7:2.8,3.4:', when='+python', type=('build', 'run'))
    depends_on('py-setuptools', when='+python', type='build')
    depends_on('py-cython', when='+python', type='build')
    depends_on('py-numpy@1.16.1:1.999', when='@1.6:+python', type=('build', 'run'))
    depends_on('py-numpy@1.8.2:1.15.0', when='@1.3.0+python', type=('build', 'run'))
    depends_on('py-requests@2.20.0:2.999', when='@1.6:+python', type=('build', 'run'))
    depends_on('py-requests@2.18.4:2.18.999', when='@1.3.0+python', type=('build', 'run'))
    depends_on('py-graphviz@0.8.1:0.8.999', when='+python', type=('build', 'run'))

    conflicts('+cudnn', when='~cuda')
    conflicts('+nccl', when='~cuda')

    patch('openblas-1.7.0.patch', when='@1.7.0:1.master')
    patch('openblas-1.6.0.patch', when='@1.6.0')
    patch('cmake_cuda_flags.patch', when='@1.6:1.7')
    patch('parallell_shuffle.patch', when='@1.6.0')

    # python/setup.py assumes libs can be found in build directory
    build_directory = 'build'
    generator = 'Ninja'

    def setup_run_environment(self, env):
        env.set('MXNET_LIBRARY_PATH', self.spec['mxnet'].libs[0])

        if self.spec.satisfies('+nccl ^nccl@2.1:'):
            env.set('NCCL_LAUNCH_MODE', 'PARALLEL')

    def cmake_args(self):
        # https://mxnet.apache.org/get_started/build_from_source
        args = [
            self.define_from_variant('USE_CUDA', 'cuda'),
            self.define_from_variant('USE_CUDNN', 'cudnn'),
            self.define_from_variant('USE_OPENCV', 'opencv'),
            self.define_from_variant('USE_OPENMP', 'openmp'),
            self.define_from_variant('USE_LAPACK', 'lapack'),
            self.define_from_variant('USE_MKLDNN', 'mkldnn'),
        ]

        if '+cuda' in self.spec:
            if 'cuda_arch=none' not in self.spec:
                cuda_arch = ';'.join('{0:.1f}'.format(float(i) / 10.0) for i
                                     in self.spec.variants['cuda_arch'].value)
                args.append(self.define('MXNET_CUDA_ARCH', cuda_arch))

            args.append(self.define_from_variant('USE_NCCL', 'nccl'))

            # Workaround for bug in GCC 8+ and CUDA 10 on PowerPC
            args.append(self.define(
                'CMAKE_CUDA_FLAGS', self.compiler.cxx11_flag))

        return args

    @run_after('build')
    def build_python(self):
        if '+python' in self.spec:
            with working_dir('python'):
                setup_py('build')

    @run_after('install')
    def install_python(self):
        if '+python' in self.spec:
            with working_dir('python'):
                setup_py('install', '--prefix={0}'.format(self.prefix),
                         '--single-version-externally-managed', '--root=/')

    def test(self):
        """Attempts to import modules of the installed package."""

        if '+python' in self.spec:
            # Make sure we are importing the installed modules,
            # not the ones in the source directory
            for module in self.import_modules:
                self.run_test(self.spec['python'].command.path,
                              ['-c', 'import {0}'.format(module)],
                              purpose='checking import of {0}'.format(module),
                              work_dir='spack-test')
