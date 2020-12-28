# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Velvet(MakefilePackage):
    """Velvet is a de novo genomic assembler specially designed for short read
       sequencing technologies."""

    homepage = "http://www.ebi.ac.uk/~zerbino/velvet/"
    url      = "http://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz"

    version('1.2.10', sha256='884dd488c2d12f1f89cdc530a266af5d3106965f21ab9149e8cb5c633c977640')

    depends_on('zlib')

    def edit(self, spec, prefix):
        if spec.target.family == 'aarch64':
            makefile = FileFilter('Makefile')
            makefile.filter('-m64', '')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('velvetg', prefix.bin)
        install('velveth', prefix.bin)
