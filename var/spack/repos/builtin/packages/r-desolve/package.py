# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RDesolve(RPackage):
    """Solvers for Initial Value Problems of Differential Equations ('ODE',
    'DAE', 'DDE')

    Functions that solve initial value problems of a system of first-order
    ordinary differential equations ('ODE'), of partial differential equations
    ('PDE'), of differential algebraic equations ('DAE'), and of delay
    differential equations.  The functions provide an interface to the FORTRAN
    functions 'lsoda', 'lsodar', 'lsode', 'lsodes' of the 'ODEPACK' collection,
    to the FORTRAN functions 'dvode', 'zvode' and 'daspk' and a
    C-implementation of solvers of the 'Runge-Kutta' family with fixed or
    variable time steps.  The package contains routines designed for solving
    'ODEs' resulting from 1-D, 2-D and 3-D partial differential equations
    ('PDE') that have been converted to 'ODEs' by numerical differencing."""

    homepage = "https://cloud.r-project.org/package=deSolve"
    url      = "https://cloud.r-project.org/src/contrib/deSolve_1.20.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/deSolve"

    version('1.28', sha256='4c55ef4cae841df91034382d277b483985af120240f87af587ff82177fdb5a49')
    version('1.24', sha256='3aa52c822abb0348a904d5bbe738fcea2b2ba858caab9f2831125d07f0d57b42')
    version('1.21', sha256='45c372d458fe4c7c11943d4c409517849b1be6782dc05bd9a74b066e67250c63')
    version('1.20', sha256='56e945835b0c66d36ebc4ec8b55197b616e387d990788a2e52e924ce551ddda2')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@1.28:', type=('build', 'run'))
