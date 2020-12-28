# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class LtrRetriever(Package):
    """LTR_retriever is a highly accurate and sensitive program for
       identification of LTR retrotransposons."""

    homepage = "https://github.com/oushujun/LTR_retriever"
    url      = "https://github.com/oushujun/LTR_retriever/archive/v2.8.7.tar.gz"

    version('2.8.7', sha256='29ca6f699c57b5e964aa0ee6c7d3e1e4cd5362dadd789e5f0e8c82fe0bb29369')

    depends_on('perl', type='run')
    depends_on('blast-plus', type='run')
    depends_on('hmmer@3.1b2:', type='run')
    depends_on('cdhit', type='run')
    depends_on('repeatmasker', type='run')

    def install(self, spec, prefix):
        filter_file(r'BLAST\+=.*', 'BLAST+=%s' % spec['blast-plus'].prefix.bin,
                    'paths')
        filter_file('RepeatMasker=.*',
                    'RepeatMasker=%s' % spec['repeatmasker'].prefix.bin,
                    'paths')
        filter_file('HMMER=.*',
                    'HMMER=%s' % spec['hmmer'].prefix.bin,
                    'paths')
        filter_file('CDHIT=.*',
                    'CDHIT=%s' % spec['cdhit'].prefix,
                    'paths')
        filter_file('BLAST=.*', '', 'paths')

        mkdirp(prefix.opt)
        mkdirp(prefix.bin)

        install_tree('.', prefix.opt.ltr_retriever)

        symlink(prefix.opt.ltr_retriever.LTR_retriever,
                prefix.bin.LTR_retriever)
