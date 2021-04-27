# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ROptimx(RPackage):
    """Expanded Replacement and Extension of the 'optim' Function:

    Provides a replacement and extension of the optim() function to call to
    several function minimization codes in R in a single statement. These
    methods handle smooth, possibly box constrained functions of several or
    many parameters. Note that function 'optimr()' was prepared to simplify the
    incorporation of minimization codes going forward. Also implements some
    utility codes and some extra solvers, including safeguarded Newton methods.
    Many methods previously separate are now included here. This is the version
    for CRAN."""

    cran     = "optimx"

    version('2020-4.2', sha256='6381c25c322287fc98ab1b2965d3f68c9a92c587c76aca1d33fd6428b2167101')

    depends_on('r-numderiv', type=('build', 'run'))
