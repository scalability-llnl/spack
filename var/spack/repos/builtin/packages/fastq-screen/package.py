# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FastqScreen(Package):
    """FastQ Screen allows you to screen a library of sequences in FastQ format
       against a set of sequence databases so you can see if the composition of
       the library matches with what you expect."""

    homepage = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/"
    url      = "https://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/fastq_screen_v0.11.2.tar.gz"

    version('0.11.2', sha256='a179df1f5803b42bbbb2b50af05ea18ae6fefcbf7020ca2feeb0d3c598a65207')

    depends_on('perl', type='run')
    depends_on('perl-gdgraph', type='run')
    depends_on('bowtie')
    depends_on('bowtie2')
    depends_on('bwa')
    depends_on('samtools')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
