# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLpsolve(RPackage):
    """Lp_solve is freely available (under LGPL 2) software for solving
       linear, integer and mixed integer programs. In this
       implementation we supply a "wrapper" function in C and some R
       functions that solve general linear/integer problems, assignment
       problems, and transportation problems. This version calls
       lp_solve"""

    homepage = "https://cloud.r-project.org/package=lpSolve"
    url      = "https://cloud.r-project.org/src/contrib/lpSolve_5.6.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lpSolve"

    version('5.6.13.2', sha256='75f0c0af5cbdc219ac29c792342ecd625903632ad86e581c408879958aa88539')
    version('5.6.13.1', sha256='6ad8dc430f72a4698fc4a615bb5ecb73690b3c4520e84d9094af51a528f720b8')
    version('5.6.13', sha256='d5d41c53212dead4fd8e6425a9d3c5767cdc5feb19d768a4704116d791cf498d')
