# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Platypus(Package):
    """A Haplotype-Based Variant Caller For Next Generation Sequence Data"""

    homepage = "http://www.well.ox.ac.uk/platypus"
    url      = "http://www.well.ox.ac.uk/bioinformatics/Software/Platypus-latest.tgz"

    version('0.8.1', sha256='a0f39e800ebdc5590e9b568a791bc6746df0fde4d1c3622140db64dea175622b')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('htslib')

    def install(self, spec, prefix):
        build_platypus = Executable('./buildPlatypus.sh')
        build_platypus()
        install_tree('.', prefix.bin)
