# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Paml(MakefilePackage):
    """PAML is a package of programs for phylogenetic analyses of DNA or
       protein sewuences using maximum likelihood."""

    homepage = "http://abacus.gene.ucl.ac.uk/software/paml.html"
    url      = "http://abacus.gene.ucl.ac.uk/software/paml4.9h.tgz"

    version('4.9h', sha256='623bf6cf4a018a4e7b4dbba189c41d6c0c25fdca3a0ae24703b82965c772edb3')

    build_directory = 'src'

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('baseml', prefix.bin)
            install('basemlg', prefix.bin)
            install('chi2', prefix.bin)
            install('codeml', prefix.bin)
            install('evolver', prefix.bin)
            install('infinitesites', prefix.bin)
            install('mcmctree', prefix.bin)
            install('pamp', prefix.bin)
            install('yn00', prefix.bin)
        install_tree('dat', prefix.dat)
        install_tree('Technical', prefix.Technical)
