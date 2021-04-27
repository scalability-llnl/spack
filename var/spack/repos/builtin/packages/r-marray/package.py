# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMarray(RPackage):
    """Exploratory analysis for two-color spotted microarray data:

    Class definitions for two-color spotted microarray data. Fuctions for data
    input, diagnostic plots, normalization and quality checking."""

    homepage = "http://www.maths.usyd.edu.au/u/jeany/"
    bioc     = "marray"

    version('1.68.0', commit='67b3080486abdba7dd19fccd7fb731b0e8b5b3f9')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
