# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDesolve(RPackage):
    """Solvers for Initial Value Problems of Differential Equations ('ODE',
    'DAE', 'DDE').

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

    cran = "deSolve"

    version("1.40", sha256="8c09ae6bb6875b569b9844eede30b790f39fc227f5c9d045fa63ce1b22f500ef")
    version("1.35", sha256="96f17f497713754f84ff56c3538c6d05b9f5229f9a2a32aafec7d7cdc721d488")
    version("1.34", sha256="2254305f44dde22ac685fef4c60e29a0608af0197c803107365d1d80b75c9f21")
    version("1.33", sha256="71de979e05ce7e472308ac5218e97efe976051364ba579b10940dc1fe4c8b684")
    version("1.32", sha256="74670f16eaafddd044a3ac1813acd5d164aed3f862b87aa1ac275b600e27d9ad")
    version("1.30", sha256="39f65d7af6b4d85eb023cce2a200c2de470644b22d45e210c5b7d558c3abf548")
    version("1.28", sha256="4c55ef4cae841df91034382d277b483985af120240f87af587ff82177fdb5a49")
    version("1.24", sha256="3aa52c822abb0348a904d5bbe738fcea2b2ba858caab9f2831125d07f0d57b42")
    version("1.21", sha256="45c372d458fe4c7c11943d4c409517849b1be6782dc05bd9a74b066e67250c63")
    version("1.20", sha256="56e945835b0c66d36ebc4ec8b55197b616e387d990788a2e52e924ce551ddda2")

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@1.28:")
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.32:")
