# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hisat2(MakefilePackage):
    """HISAT2 is a fast and sensitive alignment program for mapping
       next-generation sequencing reads (whole-genome, transcriptome, and
       exome sequencing data) against the general human population (as well as
       against a single reference genome)."""

    homepage = "https://daehwankimlab.github.io/hisat2/"
    url      = "ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/downloads/hisat2-2.1.0-source.zip"

    version('2.2.0', sha256='0dd55168853b82c1b085f79ed793dd029db163773f52272d7eb51b3b5e4a4cdd',
            url='https://cloud.biohpc.swmed.edu/index.php/s/hisat2-220-source/download',
            extension='zip')
    version('2.1.0', sha256='89a276eed1fc07414b1601947bc9466bdeb50e8f148ad42074186fe39a1ee781')

    def install(self, spec, prefix):
        if spec.satisfies('@:2.1.0'):
            install_tree('doc', prefix.doc)

        install_tree('example', prefix.example)
        install_tree('hisatgenotype_modules', prefix.hisatgenotype_modules)
        install_tree('hisatgenotype_scripts', prefix.hisatgenotype_scripts)
        install_tree('scripts', prefix.scripts)
        mkdirp(prefix.bin)
        install('hisat2', prefix.bin)
        install('hisat2-align-s', prefix.bin)
        install('hisat2-align-l', prefix.bin)
        install('hisat2-build', prefix.bin)
        install('hisat2-build-s', prefix.bin)
        install('hisat2-build-l', prefix.bin)
        install('hisat2-inspect', prefix.bin)
        install('hisat2-inspect-s', prefix.bin)
        install('hisat2-inspect-l', prefix.bin)
        install('*.py', prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix)
