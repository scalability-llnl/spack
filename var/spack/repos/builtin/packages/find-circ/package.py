# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FindCirc(Package):
    """Find-circ is a collection of python scripts
    detecting head-to-tail spliced (back-spliced) sequencing reads,
    indicative of circular RNA (circRNA) in RNA-seq data."""

    homepage = "https://github.com/marvin-jens/find_circ"
    url      = "https://github.com/marvin-jens/find_circ/archive/v1.2.tar.gz"

    version('1.2', sha256='f88bf9b5d0cc818313074982d4460c96706f555d924e2821832c3d03bf67743e')

    depends_on('python@2.7:2.8', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    # Higher version of py-pandas and py-numpy
    # depends on python@3: which conflicts with py-rnacocktail
    depends_on('py-numpy@:1.16.5', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('cmp_bed.py', prefix.bin)
        install('find_circ.py', prefix.bin)
        install('maxlength.py', prefix.bin)
        install('unmapped2anchors.py', prefix.bin)
        install('README.md', prefix)
        install('README.pdf', prefix)
        install('LICENSE', prefix)
        install_tree('test_data', prefix.test_data)
