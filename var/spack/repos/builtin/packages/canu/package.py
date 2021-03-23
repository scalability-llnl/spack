# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Canu(MakefilePackage):
    """A single molecule sequence assembler for genomes large and
       small."""

    homepage = "http://canu.readthedocs.io/"
    url      = "https://github.com/marbl/canu/archive/v1.5.tar.gz"

    version('2.0', sha256='e2e6e8b5ec4dd4cfba5e372f4a64b2c01fbd544d4b5867746021f10771a6f4ef')
    version('1.8',   sha256='30ecfe574166f54f79606038830f68927cf0efab33bdc3c6e43fd1448fa0b2e4')
    version('1.7.1', sha256='c314659c929ee05fd413274f391463a93f19b8337eabb7ee5de1ecfc061caafa')
    version('1.7',   sha256='c5be54b0ad20729093413e7e722a19637d32e966dc8ecd2b579ba3e4958d378a')
    version('1.5', sha256='06e2c6d7b9f6d325b3b468e9c1a5de65e4689aed41154f2cee5ccd2cef0d5cf6')

    depends_on('gnuplot', type='run')
    depends_on('java', type='run')
    depends_on('perl', type='run')
    # build fail when using boost@1.71.0:1.73.0 by canu@1.8:2.0
    depends_on('boost@:1.70.0')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    build_directory = 'src'
    build_targets = ['clean']

    def patch(self):
        # Use our perl, not whatever is in the environment
        filter_file(r'^#!/usr/bin/env perl',
                    '#!{0}'.format(self.spec['perl'].command.path),
                    'src/pipelines/canu.pl')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('all', 'TARGET_DIR={0}'.format(prefix))
