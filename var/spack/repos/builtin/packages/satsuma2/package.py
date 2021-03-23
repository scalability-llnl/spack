# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Satsuma2(CMakePackage):
    """Satsuma2 is an optimsed version of Satsuma, a tool to reliably align
       large and complex DNA sequences providing maximum sensitivity (to find
       all there is to find), specificity (to only find real homology) and
       speed (to accomodate the billions of base pairs in vertebrate genomes).
    """

    homepage = "https://github.com/bioinfologics/satsuma2"
    git      = "https://github.com/bioinfologics/satsuma2.git"

    version('2016-11-22', commit='da694aeecf352e344b790bea4a7aaa529f5b69e6')

    def install(self, spec, prefix):
        install_tree(join_path(self.build_directory, 'bin'), prefix.bin)
