# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastmath(BundlePackage):
    """FASTMath is a suite of ~15 numerical libraries frequently used together
    in various SciDAC and CSE applications. The suite includes discretization
    libraries for structured, AMR and unstructured grids as well as solver
    libraries for ODE's, Time Integrators, Iterative, Non-Linear, and Direct
    Solvers."""

    homepage = "https://fastmath-scidac.org/"

    version("latest")

    depends_on("amrex")  # default is 3 dimensions
    depends_on("chombo@3.2")
    depends_on("hypre~internal-superlu")
    # depends_on('ml-trilinos')  # hoping for stripped down install of just ml
    # depends_on('nox-trilinos') # hoping for stripped down install of just nox
    depends_on("mpi")
    depends_on("arpack-ng")
    depends_on("petsc")
    depends_on("phasta")
    depends_on("pumi")
    depends_on("sundials")
    depends_on("superlu-dist")
    depends_on("trilinos")
    depends_on("zoltan")
