# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBrobdingnag(RPackage):
    """Very Large Numbers in R:

    Handles very large numbers in R. Real numbers are held using their natural
    logarithms, plus a logical flag indicating sign. The package includes a
    vignette that gives a step-by-step introduction to using S4 methods."""

    homepage = "https://github.com/RobinHankin/Brobdingnag.git"
    cran     = "Brobdingnag"

    version('1.2-6', sha256='19eccaed830ce9d93b70642f6f126ac66722a98bbd48586899cc613dd9966ad4')

    depends_on('r@2.13.0:', type=('build', 'run'))
