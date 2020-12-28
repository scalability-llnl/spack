# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BppSuite(CMakePackage):
    """BppSuite is a suite of ready-to-use programs for phylogenetic and
       sequence analysis."""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/BppSuite"
    url      = "http://biopp.univ-montp2.fr/repos/sources/bppsuite/bppsuite-2.2.0.tar.gz"

    version('2.2.0', sha256='761fa5eec794af221d971ae70fd8c43171ad71a6bb5f20549263a1797b43f138')

    depends_on('cmake@2.6:', type='build')
    depends_on('texinfo', type='build')
    depends_on('bpp-core')
    depends_on('bpp-seq')
    depends_on('bpp-phyl')

    # Clarify isinf's namespace, because Fujitsu compiler can't
    # resolve ambiguous of 'isinf' function.
    patch('clarify_isinf.patch', when='%fj')
