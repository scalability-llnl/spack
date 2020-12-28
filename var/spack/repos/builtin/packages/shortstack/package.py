# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shortstack(Package):
    """ShortStack is a tool developed to process and analyze smallRNA-seq data
       with respect to a reference genome, and output a comprehensive and
       informative annotation of all discovered small RNA genes."""

    homepage = "http://sites.psu.edu/axtell/software/shortstack/"
    url      = "https://github.com/MikeAxtell/ShortStack/archive/v3.8.3.tar.gz"

    version('3.8.3', sha256='7c76f51ed949ca95ec5df7cb54803ae2350658fd64c75909351d5a856abb0dbe')

    depends_on('perl', type=('build', 'run'))
    depends_on('samtools')
    depends_on('viennarna')
    depends_on('bowtie')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('ShortStack', prefix.bin)
