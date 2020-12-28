# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mxnet(MakefilePackage):
    """MXNet is a deep learning framework
    designed for both efficiency and flexibility."""

    homepage = "http://mxnet.io"
    url      = "https://github.com/apache/incubator-mxnet/releases/download/1.3.0/apache-mxnet-src-1.3.0-incubating.tar.gz"

    maintainers = ['adamjstewart']

    version('1.6.0', sha256='01eb06069c90f33469c7354946261b0a94824bbaf819fd5d5a7318e8ee596def')
    version('1.3.0', sha256='c00d6fbb2947144ce36c835308e603f002c1eb90a9f4c5a62f4d398154eed4d2')

    variant('cuda', default=False, description='Enable CUDA support')
    variant('opencv', default=True, description='Enable OpenCV support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('profiler', default=False, description='Enable Profiler (for verification and debug only).')
    variant('python', default=True, description='Install python bindings')

    depends_on('dmlc-core@20170508')
    depends_on('dmlc-core+openmp', when='+openmp')
    depends_on('dmlc-core~openmp', when='~openmp')
    depends_on('mshadow@20170721')
    depends_on('ps-lite@20170328')
    depends_on('nnvm~shared@20170418')
    depends_on('blas')
    depends_on('cudnn', when='+cuda')
    depends_on('cudnn', when='+cuda')
    depends_on('cub', when='+cuda')
    depends_on('opencv+core+imgproc+highgui+jpeg+png+tiff~eigen~ipp@3.0:3.4.99', when='@1.3.0 +opencv')
    depends_on('opencv+core+imgproc+highgui+jpeg+png+tiff~eigen~ipp@3.0:', when='+opencv')

    # python extensions
    depends_on('python@2.7:', type=('build', 'run'), when='+python')
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-numpy@:1.15.0', type=('build', 'run'), when='@1.3.0 +python')
    depends_on('py-numpy@1.16:', type=('build', 'run'), when='@1.6.0 +python')
    extends('python', when='+python')

    patch('makefile.patch', when='@0.10:0.11')
    patch('makefile.opencv.patch', when='@1.6.0')
    patch('parallell_shuffle.patch', when='@1.6.0')

    def build(self, spec, prefix):
        # copy template configuration file
        copy('make/config.mk', 'config.mk')

        # remove compiler overrides
        filter_file('export CC = gcc', '', 'config.mk', string=True)
        filter_file('export CXX = g++', '', 'config.mk', string=True)

        # add blas prefix to include paths
        filter_file(
            '-I$(NNVM_PATH)/include',
            '-I$(NNVM_PATH)/include -I%s/include' % spec['blas'].prefix,
            'Makefile', string=True
        )

        # mxnet comes with its own version of nnvm and dmlc.
        # building it will fail if we use the spack paths

        args = [
            'CC=%s' % self.compiler.cc,
            'CXX=%s' % self.compiler.cxx,
            'MSHADOW_PATH=%s' % spec['mshadow'].prefix,
            'PS_PATH=%s' % spec['ps-lite'].prefix,
            'USE_OPENMP=%s' % ('1' if '+openmp' in spec else '0'),
            'USE_CUDA=%s' % ('1' if '+cuda' in spec else '0'),
            'USE_CUDNN=%s' % ('1' if '+cuda' in spec else '0'),
            'USE_OPENCV=%s' % ('1' if '+opencv' in spec else '0'),
            'USE_PROFILER=%s' % ('1' if '+profiler' in spec else '0'),
        ]

        if '+opencv' in spec:
            if spec.satisfies('@1.3.0'):
                filter_file(
                    '$(shell pkg-config --cflags opencv)',
                    spec['opencv'].headers.include_flags,
                    'Makefile', string=True
                )
                filter_file(
                    '$(filter-out -lopencv_ts, '
                    '$(shell pkg-config --libs opencv))',
                    spec['opencv'].libs.link_flags,
                    'Makefile', string=True
                )
            else:
                args.extend(
                    ['USE_OPENCV_INC_PATH=' +
                        spec['opencv'].headers.directories[0],
                     'USE_OPENCV_LIB_PATH=' +
                        spec['opencv'].libs.directories[0]]
                )

        if 'openblas' in spec:
            args.extend(['USE_BLAS=openblas'])
        elif 'atlas' in spec or 'cblas' in spec:
            args.extend(['USE_BLAS=atlas'])
        else:
            args.extend(['USE_BLAS=blas'])

        if '+cuda' in spec:
            args.extend(['USE_CUDA_PATH=%s' % spec['cuda'].prefix,
                         'CUDNN_PATH=%s' % spec['cudnn'].prefix,
                         'CUB_INCLUDE=%s' % spec['cub'].prefix.include])

        make(*args)

    def install(self, spec, prefix):
        # mxnet is just a shared library -- no need to install a bin tree

        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)

        # install python bindings
        if '+python' in spec:
            python = which('python')
            python('python/setup.py', 'install', '--prefix={0}'.format(prefix))
