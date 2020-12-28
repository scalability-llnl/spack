# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Faiss(AutotoolsPackage, CudaPackage):
    """Faiss is a library for efficient similarity search and clustering of
       dense vectors.

      Faiss contains algorithms that search in sets of vectors of any size, up
      to ones that possibly do not fit in RAM. It also contains supporting code
      for evaluation and parameter tuning. Faiss is written in C++ with
      complete wrappers for Python/numpy. Some of the most useful algorithms
      are implemented on the GPU. It is developed by Facebook AI Research.
    """

    homepage = "https://github.com/facebookresearch/faiss"
    url      = "https://github.com/facebookresearch/faiss/archive/v1.6.3.tar.gz"

    maintainers = ['bhatiaharsh']

    version('1.6.3', sha256='e1a41c159f0b896975fbb133e0240a233af5c9286c09a28fde6aefff5336e542')
    version('1.5.3', sha256='b24d347b0285d01c2ed663ccc7596cd0ea95071f3dd5ebb573ccfc28f15f043b')

    variant('python', default=False, description='Build Python bindings')
    variant('tests',  default=False, description='Build Tests')

    conflicts('+tests', when='~python', msg='+tests must be accompanied by +python')

    depends_on('python@3.7:',   when='+python', type=('build', 'run'))
    depends_on('py-numpy',      when='+python', type=('build', 'run'))
    depends_on('py-scipy',      when='+tests',  type=('build', 'run'))

    depends_on('blas')
    depends_on('py-setuptools', when='+python', type='build')
    depends_on('swig',          when='+python', type='build')

    # patch for v1.5.3
    # faiss assumes that the "source directory" will always
    # be called "faiss" (not spack-src or faiss-1.5.3)
    # so, we will have to create a symlink to self (faiss did that in 1.6.3)
    # and add an include path
    patch('fixes-in-v1.5.3.patch', when='@1.5.3')

    # patch for v1.6.3
    # for v1.6.3, GPU build has a bug (two files need to be deleted)
    # https://github.com/facebookresearch/faiss/issues/1159
    # also, some include paths in gpu/tests/Makefile are missing
    patch('fixes-in-v1.6.3.patch', when='@1.6.3')

    def configure_args(self):
        args = []
        args.extend(self.with_or_without('cuda', activation_value='prefix'))
        return args

    def build(self, spec, prefix):

        make()

        if '+python' in self.spec:
            make('-C', 'python')

        # CPU tests
        if '+tests' in self.spec:
            with working_dir('tests'):
                make('gtest')
                make('tests')

        # GPU tests
        if '+tests+cuda' in self.spec:
            with working_dir(os.path.join('gpu', 'test')):
                make('gtest')
                make('build')                       # target added by the patch
                make('demo_ivfpq_indexing_gpu')

    def install(self, spec, prefix):

        make('install')

        if '+python' in self.spec:
            with working_dir('python'):
                setup_py('install', '--prefix=' + prefix,
                         '--single-version-externally-managed', '--root=/')

        if '+tests' not in self.spec:
            return

        if not os.path.isdir(self.prefix.bin):
            os.makedirs(self.prefix.bin)

        def _prefix_and_install(file):
            os.rename(file, 'faiss_' + file)
            install('faiss_' + file, self.prefix.bin)

        # CPU tests
        with working_dir('tests'):
            # rename the exec to keep consistent with gpu tests
            os.rename('tests', 'TestCpu')
            _prefix_and_install('TestCpu')

        # GPU tests
        if '+cuda' in self.spec:
            with working_dir(os.path.join('gpu', 'test')):
                _prefix_and_install('TestGpuIndexFlat')
                _prefix_and_install('TestGpuIndexBinaryFlat')
                _prefix_and_install('TestGpuIndexIVFFlat')
                _prefix_and_install('TestGpuIndexIVFPQ')
                _prefix_and_install('TestGpuMemoryException')
                _prefix_and_install('TestGpuSelect')
                _prefix_and_install('demo_ivfpq_indexing_gpu')

    @run_after('configure')
    def _fix_makefile(self):

        # spack injects its own optimization flags
        makefile = FileFilter('makefile.inc')
        makefile.filter('CPUFLAGS     = -mavx2 -mf16c',
                        '#CPUFLAGS     = -mavx2 -mf16c')

    def setup_run_environment(self, env):
        if '+python' in self.spec:
            env.prepend_path('PYTHONPATH', site_packages_dir)
