# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Pmerge(AutotoolsPackage):
    """PMERGE implements a new method that identifies candidate PSVs by
       building networks of loci that share high levels of nucleotide
       similarity. The PMERGE is embedded in the analysis pipeline of the
       widely used Stacks software, and it is straightforward to apply it as
       an additional filter in population-genomic studies using RAD-seq
       data."""

    homepage = "https://github.com/beiko-lab/PMERGE"
    git      = "https://github.com/beiko-lab/PMERGE.git"

    version('master',  branch='master')

    depends_on('automake@1.14:1.14.99', type='build')
    depends_on('autoconf', type='build')
    depends_on('m4', type='build')
    depends_on('perl', type='build')

    @property
    def configure_directory(self):
        return 'Install'
