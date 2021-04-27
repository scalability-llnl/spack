# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Samtools(Package):
    """SAM Tools provide various utilities for manipulating alignments in
       the SAM format, including sorting, merging, indexing and generating
       alignments in a per-position format"""

    homepage = "http://www.htslib.org"
    url      = "https://github.com/samtools/samtools/releases/download/1.3.1/samtools-1.3.1.tar.bz2"

    version('1.12', sha256='6da3770563b1c545ca8bdf78cf535e6d1753d6383983c7929245d5dba2902dcb')
    version('1.10', sha256='7b9ec5f05d61ec17bd9a82927e45d8ef37f813f79eb03fe06c88377f1bd03585')
    version('1.9', sha256='083f688d7070082411c72c27372104ed472ed7a620591d06f928e653ebc23482')
    version('1.8', sha256='c942bc1d9b85fd1b05ea79c5afd2805d489cd36b2c2d8517462682a4d779be16')
    version('1.7', sha256='e7b09673176aa32937abd80f95f432809e722f141b5342186dfef6a53df64ca1')
    version('1.6', sha256='ee5cd2c8d158a5969a6db59195ff90923c662000816cc0c41a190b2964dbe49e')
    version('1.5', sha256='8542da26832ee08c1978713f5f6188ff750635b50d8ab126a0c7bb2ac1ae2df6')
    version('1.4', sha256='9aae5bf835274981ae22d385a390b875aef34db91e6355337ca8b4dd2960e3f4')
    version('1.3.1', sha256='6c3d74355e9cf2d9b2e1460273285d154107659efa36a155704b1e4358b7d67e')
    version('1.2', sha256='420e7a4a107fe37619b9d300b6379452eb8eb04a4a9b65c3ec69de82ccc26daa')
    version('0.1.8', sha256='343daf96f035c499c5b82dce7b4d96b10473308277e40c435942b6449853815b',
            url="https://github.com/samtools/samtools/archive/0.1.8.tar.gz")

    depends_on('zlib')
    depends_on('ncurses')
    depends_on('perl', type='run')
    depends_on('python', type='run')

    # htslib became standalone @1.3.1, must use corresponding version
    depends_on('htslib@1.12', when='@1.12')
    depends_on('htslib@1.10.2', when='@1.10')
    depends_on('htslib@1.9', when='@1.9')
    depends_on('htslib@1.8', when='@1.8')
    depends_on('htslib@1.7', when='@1.7')
    depends_on('htslib@1.6', when='@1.6')
    depends_on('htslib@1.5', when='@1.5')
    depends_on('htslib@1.4', when='@1.4')
    depends_on('htslib@1.3.1', when='@1.3.1')

    def install(self, spec, prefix):
        if '+termlib' in spec['ncurses']:
            curses_lib = '-lncursesw -ltinfow'
        else:
            curses_lib = '-lncursesw'

        if self.spec.version >= Version('1.3.1'):
            configure('--prefix={0}'.format(prefix),
                      '--with-htslib={0}'.format(self.spec['htslib'].prefix),
                      '--with-ncurses',
                      'CURSES_LIB={0}'.format(curses_lib))
            make()
            make('install')
        else:
            make('prefix={0}'.format(prefix),
                 'LIBCURSES={0}'.format(curses_lib))
            if self.spec.version == Version('0.1.8'):
                make('prefix={0}'.format(prefix))
            else:
                make('prefix={0}'.format(prefix), 'install')

        # Install dev headers and libs for legacy apps depending on them
        mkdir(prefix.include)
        mkdir(prefix.lib)
        install('sam.h', prefix.include)
        install('bam.h', prefix.include)
        install('libbam.a', prefix.lib)
