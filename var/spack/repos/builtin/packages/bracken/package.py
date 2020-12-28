# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Bracken(Package):
    """Bracken (Bayesian Reestimation of Abundance with KrakEN) is a highly
    accurate statistical method that computes the abundance of species in DNA
    sequences from a metagenomics sample."""

    homepage = "https://ccb.jhu.edu/software/bracken"
    url      = "https://github.com/jenniferlu717/Bracken/archive/1.0.0.tar.gz"

    version('1.0.0', sha256='8ee736535ad994588339d94d0db4c0b1ba554a619f5f96332ee09f2aabdfe176')

    depends_on('perl', type=('build', 'link', 'run'))
    depends_on('python@2.7:', type=('build', 'link', 'run'))
    depends_on('perl-exporter-tiny')
    depends_on('perl-list-moreutils')
    depends_on('perl-parallel-forkmanager')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree('sample_data', prefix.sample_data)

        filter_file(
            r'#!/bin/env perl',
            '#!/usr/bin/env perl',
            'count-kmer-abundances.pl'
        )

        filter_file(
            r'#!/usr/bin/python',
            '#!/usr/bin/env {0}'.format(
                os.path.basename(self.spec['python'].command.path)),
            'est_abundance.py'
        )

        filter_file(
            r'#!/usr/bin/python',
            '#!/usr/bin/env {0}'.format(
                os.path.basename(self.spec['python'].command.path)),
            'generate_kmer_distribution.py'
        )

        files = (
            'count-kmer-abundances.pl',
            'est_abundance.py',
            'generate_kmer_distribution.py',
        )

        chmod = which('chmod')
        for name in files:
            install(name, prefix.bin)
            chmod('+x', join_path(self.prefix.bin, name))
