# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDnacopy(RPackage):
    """DNA copy number data analysis.

       Implements the circular binary segmentation (CBS) algorithm to segment
       DNA copy number data and identify genomic regions with abnormal copy
       number."""

    homepage = "https://bioconductor.org/packages/DNAcopy"
    git      = "https://git.bioconductor.org/packages/DNAcopy.git"

    version('1.58.0', commit='1954745eafca990d6ddeefe84059c54a8c37df23')
    version('1.56.0', commit='e521826f2515b309921272f65db421cbe2ff961a')
    version('1.54.0', commit='fe2657936afbce8ee03221461dff4265e3ded4c4')
    version('1.52.0', commit='2632fbecec4cef3705b85676942a59188ae9bba4')
    version('1.50.1', commit='a20153029e28c009df813dbaf13d9f519fafa4e8')
