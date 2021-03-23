# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Cntk(Package):
    """The Microsoft Cognitive Toolkit is a unified deep-learning toolkit
    that describes neural networks as a series of computational steps
    via a directed graph."""

    homepage = "https://www.microsoft.com/en-us/research/product/cognitive-toolkit"
    url      = "https://github.com/Microsoft/CNTK/archive/v2.0.tar.gz"
    git      = "https://github.com/Microsoft/CNTK.git"

    version('master', branch='master')
    version('2.0', sha256='3adee17f166e2a682dfb551ca017ae5c3836ca9772c0af14215a7e76254f201c')

    variant('opencv', default=False, description="Enable OpenCV support.")
    variant('kaldi', default=False, description="Enable Kaldi support.")
    variant('asgd', default=True, description="Enable DataParallelASGD powered by Multiverso.")
    variant('1bitsgd', default=False, description="Enable 1bitsgd support.")
    variant('cuda', default=False, description="Enable CUDA support.")
    variant('debug', default=False, description="Debug build.")

    depends_on('libzip')
    depends_on('openblas')
    depends_on('mpi')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('protobuf')
    # CNTK depends on kaldi@c02e8.
    # See https://github.com/Microsoft/CNTK/blob/master/Tools/docker/CNTK-CPUOnly-Image/Dockerfile#L105-L125
    depends_on('kaldi@c024e8', when='+kaldi')
    depends_on('opencv', when='+opencv')
    depends_on('cuda', when='+cuda')
    depends_on('cub@1.4.1', when='+cuda')
    depends_on('cudnn@5.1', when='+cuda')
    depends_on('nccl', when='+cuda')
    depends_on('cntk1bitsgd@c8b77d', when='+1bitsgd')
    depends_on('multiverso@143187', when='+asgd')

    # Patch CNTN's build process to use libs installed outside CNTK source tree
    # multiverso, kaldi, openfst
    patch('build.patch')
    # Patch to fix BLAS inconsistency between CNTK and KaldiReader
    patch('kaldireader-openblas.patch')
    # Patch to change behaviour of lock file - https://github.com/Microsoft/CNTK/issues/62
    patch('lock-file.patch')

    def install(self, spec, prefix):
        args = []

        args.append('--with-mpi=' + spec['mpi'].prefix)
        args.append('--with-openblas=' + spec['openblas'].prefix)
        args.append('--with-libzip=' + spec['libzip'].prefix)
        args.append('--with-boost=' + spec['boost'].prefix)
        args.append('--with-protobuf=' + spec['protobuf'].prefix)

        if '+debug' in spec:
            args.append('--with-buildtype=debug')
        else:
            args.append('--with-buildtype=release')

        if '+1bitsgd' in spec:
            args.append('--1bitsgd=yes')
            args.append('--with-1bitsgd={0}/include'
                        .format(spec['cntk1bitsgd'].prefix))

        if '+asgd' in spec:
            args.append('--asgd=yes')
            args.append('--with-multiverso={0}'
                        .format(spec['multiverso'].prefix))
        else:
            args.append('--asgd=no')

        if '+opencv' in spec:
            args.append('--with-opencv=' + spec['opencv'].prefix)

        if '+kaldi' in spec:
            args.append('--with-kaldi=' + spec['kaldi'].prefix)
            args.append('--with-openfst=' + spec['openfst'].prefix)

        if '+cuda' in spec:
            args.append('--cuda=yes')
            args.append('--with-cuda={0}'.format(spec['cuda'].prefix))
            args.append('--with-cub={0}'
                        .format(spec['cub'].prefix.include))
            args.append('--with-cudnn={0}'
                        .format(spec['cudnn'].prefix))
            args.append('--with-nccl={0}'.format(spec['nccl'].prefix))
            args.append('--with-gdk-include={0}'
                        .format(spec['cuda'].prefix.include))
            args.append('--with-gdk-nvml-lib={0}/stubs'
                        .format(spec['cuda'].prefix.lib64))

        configure(*args)

        make()

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('Examples', join_path(prefix, 'Examples'))
        install_tree('Tutorials', join_path(prefix, 'Tutorials'))
