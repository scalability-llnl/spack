# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lastz(MakefilePackage):
    """LASTZ is a program for aligning DNA sequences, a pairwise aligner."""

    homepage = "https://lastz.github.io/lastz"
    url      = "https://github.com/lastz/lastz/archive/1.04.00.tar.gz"

    version('1.04.03', sha256='c58ed8e37c4b0e82492b3a2b3e12447a3c40286fb8358906d19f10b0a713e9f4')
    version('1.04.00', sha256='a4c2c7a77430387e96dbc9f5bdc75874334c672be90f5720956c0f211abf9f5a')

    # Ref: https://github.com/lastz/lastz/commit/20aa14f483265b4eac97f25aca666c708b9655e4
    patch('sequences.c.patch', when='@:1.04.03')

    # set compile commands for each compiler
    def edit(self, spec, prefix):
        filter_file('gcc', spack_cc, 'src/Makefile')

    def install(self, spec, prefix):
        make('install', 'LASTZ_INSTALL={0}'.format(prefix.bin))
