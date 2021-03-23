# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from spack import *


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
    url = "https://github.com/davidemms/OrthoFinder/releases/download/2.5.2/OrthoFinder_source.tar.gz"

    version('2.5.2', sha256='e0752b66866e23a11f0592e880fac5f67258f9cf926f926dec8849564c41b8f7')
    version('2.2.0', sha256='375f711086b44e2118d7d460821294744245e254e5fa2151dfe73100c0707a8c')

    depends_on('py-numpy', type='run')
    depends_on('py-scipy', type='run')
    depends_on('diamond', type='run')
    depends_on('blast-plus', type='run')
    depends_on('mcl', type='run')
    depends_on('fastme', type='run')

    def url_for_version(self, version):
        if '@:2.3.6' in self.spec:
            url = "https://github.com/davidemms/OrthoFinder/releases/download/{0}/OrthoFinder-{0}_source.tar.gz"
            return url.format(version)
        else:
            url = "https://github.com/davidemms/OrthoFinder/releases/download/{0}/OrthoFinder_source.tar.gz"
            return url.format(version)

    def install(self, spec, prefix):
        if '@2.2.0' in spec:
            install_tree('./orthofinder', prefix.bin)
        else:
            install_tree('.', prefix.bin)
            shutil.rmtree(prefix.bin.scripts_of.bin)
        os.rename('%s/orthofinder.py' % prefix.bin, '%s/orthofinder' % prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', prefix.bin)
        env.prepend_path('PATH', prefix.bin.tools)
