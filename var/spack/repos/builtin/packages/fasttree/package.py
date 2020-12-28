# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fasttree(Package):
    """FastTree infers approximately-maximum-likelihood phylogenetic
       trees from alignments of nucleotide or protein sequences.
       FastTree can handle alignments with up to a million of sequences
       in a reasonable amount of time and memory."""

    homepage = "http://www.microbesonline.org/fasttree"
    url      = "http://www.microbesonline.org/fasttree/FastTree-2.1.10.c"

    version('2.1.10', sha256='54cb89fc1728a974a59eae7a7ee6309cdd3cddda9a4c55b700a71219fc6e926d', expand=False, url='http://www.microbesonline.org/fasttree/FastTree-2.1.10.c')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        cc = Executable(spack_cc)
        cc('-O3', self.compiler.openmp_flag,
           '-DOPENMP', '-finline-functions', '-funroll-loops', '-Wall',
           '-oFastTreeMP', 'FastTree-' + format(spec.version.dotted) + '.c',
           '-lm')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('FastTreeMP', prefix.bin)
