# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
from glob import glob


class Libxsmm(MakefilePackage):
    """Library targeting Intel Architecture
    for specialized dense and sparse matrix operations,
    and deep learning primitives."""

    homepage = 'https://github.com/hfp/libxsmm'
    url      = 'https://github.com/hfp/libxsmm/archive/1.16.1.tar.gz'
    git      = 'https://github.com/hfp/libxsmm.git'

    maintainers = ['hfp']

    version('master', branch='master')
    version('1.16.1', sha256='93dc7a3ec40401988729ddb2c6ea2294911261f7e6cd979cf061b5c3691d729d')
    version('1.16',   sha256='4f4f2ad97815413af80821d2e306eb6f00541941ad412662da05c02361a20e07')
    version('1.15',   sha256='499e5adfbf90cd3673309243c2b56b237d54f86db2437e1ac06c8746b55ab91c')
    version('1.14',   sha256='9c0af4509ea341d1ee2c6c19fc6f19289318c3bd4b17844efeb9e7f9691abf76')
    version('1.13',   sha256='47c034e169820a9633770eece0e0fdd8d4a744e09b81da2af8c2608a4625811e')
    version('1.12.1', sha256='3687fb98da00ba92cd50b5f0d18b39912c7886dad3856843573aee0cb34e9791')
    version('1.12',   sha256='37432fae4404ca12d8c5a205bfec7f9326c2d607d9ec37680f42dae60b52382a')
    version('1.11',   sha256='5fc1972471cd8e2b8b64ea017590193739fc88d9818e3d086621e5c08e86ea35')
    version('1.10',   sha256='2904f7983719fd5c5af081121c1d028d45b10b854aec9a9e67996a0602631abc')
    version('1.9',    sha256='cd8532021352b4a0290d209f7f9bfd7c2411e08286a893af3577a43457287bfa')
    version('1.8.3',  sha256='08ed4a67731d07c739fa83c426a06a5a8fe576bc273da4bab84eb0d1f4405011')
    version('1.8.2',  sha256='252ab73e437f5fcc87268df1ac130ffe6eb41e4281d9d3a3eaa7d591a85a612f')
    version('1.8.1',  sha256='2ade869c3f42f23b5263c7d594aa3c7e5e61ac6a3afcaf5d6e42899d2a7986ce')
    version('1.8',    sha256='0330201afb5525d0950ec861fec9dd75eb40a03845ebe03d2c635cf8bfc14fea')
    version('1.7.1',  sha256='9d3f63ce3eed62f04e4036de6f2be2ce0ff07781ca571af6e0bf85b077edf17a')
    version('1.7',    sha256='2eea65624a697e74b939511cd2a686b4c957e90c99be168fe134d96771e811ad')
    version('1.6.6',  sha256='7c048a48e17f7f14a475be7b83e6e941289e03debb42ce9e02a06353412f9f2a')
    version('1.6.5',  sha256='5231419a8e13e7a6d286cf25d32a3aa75c443a625e5ea57024d36468bc3d5936')
    version('1.6.4',  sha256='3788bf1cdb60f119f8a04ed7ed96861322e539ce2d2ea977f00431d6b2b80beb')
    version('1.6.3',  sha256='afad4f75ec5959bc3b18b741f3f16864f699c8b763598d01faf6af029dded48c')
    version('1.6.2',  sha256='c1ad21dee1239c9c2422b2dd2dc83e7a364909fc82ff9bd6ce7d9c73ee4569de')
    version('1.6.1',  sha256='1dd81077b186300122dc8a8f1872c21fd2bd9b88286ab9f068cc7b62fa7593a7')
    version('1.6',    sha256='c2a56f8cdc2ab03a6477ef98dbaa00917674fda59caa2824a1a29f78d2255ba5')
    version('1.5.2',  sha256='a037b7335932921960d687ef3d49b50ee38a83e0c8ad237bc20d3f4a0523f7d3')
    version('1.5.1',  sha256='9e2a400e63b6fb2d4954e53536090eb8eb6f0ca25d0f34dd3a4f166802aa3d54')
    version('1.5',    sha256='c52568c5e0e8dc9d8fcf869a716d73598e52f71c3d83af5a4c0b3be81403b423')
    version('1.4.4',  sha256='bf4a0fff05cf721e11cb6cdb74f3d27dd0fa67ccc024055f2d9dd5dbd928c7c0')
    version('1.4.3',  sha256='5033c33038ba4a75c675387aeb7c86b629e43ffc0a40df0b78e4ed52e4b5bd90')
    version('1.4.2',  sha256='9c89391635be96759486a245365793bc4593859e6d7957b37c39a29f9b4f95eb')
    version('1.4.1',  sha256='c19be118694c9b4e9a61ef4205b1e1a7e0c400c07f9bce65ae430d2dc2be5fe1')
    version('1.4',    sha256='cf483a370d802bd8800c06a12d14d2b4406a745c8a0b2c8722ccc992d0cd72dd')

    variant('shared', default=False,
            description='With shared libraries (and static libraries).')
    variant('debug', default=False,
            description='With call-trace (LIBXSMM_TRACE); unoptimized.')
    variant('header-only', default=False,
            description='With header-only installation')
    variant('generator', default=False,
            description='With generator executable(s)')
    conflicts('+header-only', when='@:1.6.2',
              msg='Header-only is available since v1.6.2!')
    depends_on('python', type='build')

    @property
    def libs(self):
        result = find_libraries(['libxsmm', 'libxsmmf'], root=self.prefix,
                                recursive=True)
        if len(result) == 0:
            result = find_libraries(['libxsmm', 'libxsmmf'], root=self.prefix,
                                    shared=False, recursive=True)
        return result

    def build(self, spec, prefix):
        # include symbols by default
        make_args = [
            'CC={0}'.format(spack_cc),
            'CXX={0}'.format(spack_cxx),
            'FC={0}'.format(spack_fc),
            'PREFIX=%s' % prefix,
            'SYM=1'
        ]

        # JIT (AVX and later) makes MNK, M, N, or K spec. superfluous
        # make_args += ['MNK=1 4 5 6 8 9 13 16 17 22 23 24 26 32']

        # include call trace as the build is already de-optimized
        if '+debug' in spec:
            make_args += ['DBG=1']
            make_args += ['TRACE=1']

        if '+shared' in spec:
            make(*(make_args + ['STATIC=0']))

        # builds static libraries by default
        make(*make_args)

    def install(self, spec, prefix):
        install_tree('include', prefix.include)

        # move pkg-config files to their right place
        mkdirp('lib/pkgconfig')
        for pcfile in glob('lib/*.pc'):
            os.rename(pcfile, os.path.join('lib/pkgconfig',
                                           os.path.basename(pcfile)))

        # always install libraries
        install_tree('lib', prefix.lib)

        if '+header-only' in spec:
            install_tree('src', prefix.src)

        if '+generator' in spec:
            install_tree('bin', prefix.bin)

        mkdirp(prefix.doc)
        install(join_path('documentation', '*.md'), prefix.doc)
        install(join_path('documentation', '*.pdf'), prefix.doc)
        if '@1.8.2:' in spec:
            install('LICENSE.md', prefix.doc)
        else:
            install('README.md', prefix.doc)
            install('LICENSE', prefix.doc)
        install('version.txt', prefix.doc)
