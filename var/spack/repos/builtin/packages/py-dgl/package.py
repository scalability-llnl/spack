# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyDgl(CMakePackage):
    """Deep Graph Library (DGL).

    DGL is an easy-to-use, high performance and scalable Python package for
    deep learning on graphs. DGL is framework agnostic, meaning if a deep graph
    model is a component of an end-to-end application, the rest of the logics
    can be implemented in any major frameworks, such as PyTorch, Apache MXNet
    or TensorFlow."""

    homepage = "https://www.dgl.ai/"
    git      = "https://github.com/dmlc/dgl.git"

    maintainers = ['adamjstewart']

    version('master', branch='master', submodules=True)
    version('0.4.3', tag='0.4.3', submodules=True)
    version('0.4.2', tag='0.4.2', submodules=True)

    variant('cuda',   default=True, description='Build with CUDA')
    variant('openmp', default=True, description='Build with OpenMP')
    variant('backend', default='pytorch', description='Default backend',
            values=['pytorch', 'mxnet', 'tensorflow'], multi=False)

    depends_on('cmake@3.5:', type='build')
    depends_on('cuda', when='+cuda')
    depends_on('llvm-openmp', when='%apple-clang +openmp')

    # Python dependencies
    # See python/setup.py
    extends('python')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.14.0:', type=('build', 'run'))
    depends_on('py-scipy@1.1.0:', type=('build', 'run'))
    depends_on('py-networkx@2.1:', type=('build', 'run'))
    depends_on('py-requests@2.19.0:', when='@0.4.3:', type=('build', 'run'))

    # Backends
    # See https://github.com/dmlc/dgl#installation
    depends_on('py-torch@1.2.0:', when='@0.4.3: backend=pytorch', type='run')
    depends_on('py-torch@0.4.1:', when='backend=pytorch', type='run')
    depends_on('mxnet@1.5.1:', when='@0.4.3: backend=pytorch', type='run')
    depends_on('mxnet@1.5.0:', when='backend=mxnet', type='run')
    depends_on('py-tensorflow@2.1:', when='@0.4.3: backend=tensorflow', type='run')
    depends_on('py-tensorflow@2.0:', when='backend=tensorflow', type='run')
    depends_on('py-tfdlpack', when='backend=tensorflow', type='run')

    build_directory = 'build'

    # https://docs.dgl.ai/install/index.html#install-from-source
    def cmake_args(self):
        args = []

        if '+cuda' in self.spec:
            args.append('-DUSE_CUDA=ON')
        else:
            args.append('-DUSE_CUDA=OFF')

        if '+openmp' in self.spec:
            args.append('-DUSE_OPENMP=ON')

            if self.spec.satisfies('%apple-clang'):
                args.extend([
                    '-DOpenMP_CXX_FLAGS=' +
                    self.spec['llvm-openmp'].headers.include_flags,
                    '-DOpenMP_CXX_LIB_NAMES=' +
                    self.spec['llvm-openmp'].libs.names[0],
                    '-DOpenMP_C_FLAGS=' +
                    self.spec['llvm-openmp'].headers.include_flags,
                    '-DOpenMP_C_LIB_NAMES=' +
                    self.spec['llvm-openmp'].libs.names[0],
                    '-DOpenMP_omp_LIBRARY=' +
                    self.spec['llvm-openmp'].libs[0],
                ])
        else:
            args.append('-DUSE_OPENMP=OFF')

        if self.run_tests:
            args.append('-DBUILD_CPP_TEST=ON')
        else:
            args.append('-DBUILD_CPP_TEST=OFF')

        return args

    def install(self, spec, prefix):
        with working_dir('python'):
            setup_py('install', '--prefix=' + prefix,
                     '--single-version-externally-managed', '--root=/')

        # Work around installation bug: https://github.com/dmlc/dgl/issues/1379
        install_tree(prefix.dgl, prefix.lib)

    def setup_run_environment(self, env):
        # https://docs.dgl.ai/install/backend.html
        backend = self.spec.variants['backend'].value
        env.set('DGLBACKEND', backend)

    @property
    def import_modules(self):
        modules = [
            'dgl', 'dgl.nn', 'dgl.runtime', 'dgl.backend', 'dgl.function',
            'dgl.contrib', 'dgl._ffi', 'dgl.data', 'dgl.runtime.ir',
            'dgl.backend.numpy', 'dgl.contrib.sampling', 'dgl._ffi._cy2',
            'dgl._ffi._cy3', 'dgl._ffi._ctypes',
        ]

        if 'backend=pytorch' in self.spec:
            modules.extend([
                'dgl.nn.pytorch', 'dgl.nn.pytorch.conv', 'dgl.backend.pytorch'
            ])
        elif 'backend=mxnet' in self.spec:
            modules.extend([
                'dgl.nn.mxnet', 'dgl.nn.mxnet.conv', 'dgl.backend.mxnet'
            ])
        elif 'backend=tensorflow' in self.spec:
            modules.extend([
                'dgl.nn.tensorflow', 'dgl.nn.tensorflow.conv',
                'dgl.backend.tensorflow'
            ])

        return modules

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                python('-c', 'import {0}'.format(module))
