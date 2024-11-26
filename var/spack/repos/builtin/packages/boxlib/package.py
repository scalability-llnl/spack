# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Boxlib(CMakePackage):
    """BoxLib, a software framework for massively parallel
    block-structured adaptive mesh refinement (AMR) codes."""

    homepage = "https://ccse.lbl.gov/BoxLib/"
    url = "https://github.com/BoxLib-Codes/BoxLib/archive/16.12.2.tar.gz"

    license("BSD-3-Clause-LBNL")

    version("16.12.2", sha256="e87faeccfcb14b3436d36c45fcd9f46ea20f65298d35c6db2a80d6332b036dd2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    variant(
        "dims",
        default="3",
        values=("1", "2", "3"),
        multi=False,
        description="Number of spatial dimensions",
    )

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend(
            [
                "-DBL_SPACEDIM=%d" % int(spec.variants["dims"].value),
                "-DBL_USE_PARTICLES=1",
                "-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON",
                "-DENABLE_FBASELIB=ON",
                "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
                "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
            ]
        )

        return options
