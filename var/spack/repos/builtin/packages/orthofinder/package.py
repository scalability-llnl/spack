# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Orthofinder(Package):
    """OrthoFinder is a fast, accurate and comprehensive analysis tool for
    comparative genomics.

    It finds orthologues and orthogroups infers rooted  gene trees for all
    orthogroups and infers a rooted species tree for the species being
    analysed. OrthoFinder also provides comprehensive statistics for
    comparative genomic analyses. OrthoFinder is simple to use and all you
    need to run it is a set of protein sequence files (one per species)
    in FASTA format."""

    homepage = "https://github.com/davidemms/OrthoFinder"
    url      = "https://github.com/davidemms/OrthoFinder/releases/download/2.2.0/OrthoFinder-2.2.0.tar.gz"

    version('2.2.0', sha256='7314f3fdfb24d84aa5b9ee27ce9f670df314889c12b8100e4e476c2d21a1c8e7')

    depends_on('blast-plus', type='run')
    depends_on('mcl', type='run')
    depends_on('fastme', type='run')
    depends_on('py-dlcpar', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.bin, 'orthofinder'))
