# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pflotran(AutotoolsPackage):
    """PFLOTRAN is an open source, state-of-the-art massively parallel
    subsurface flow and reactive transport code.
    """

    homepage = "https://www.pflotran.org"
    git = "https://bitbucket.org/pflotran/pflotran.git"

    maintainers("ghammond86", "balay")

    license("LGPL-3.0-only")

    version("develop")
    version("5.0.0", commit="f0fe931c72c03580e489724afeb8c5451406b942")  # tag v5.0.0
    version("4.0.1", commit="fd351a49b687e27f46eae92e9259156eea74897d")  # tag v4.0.1
    version("3.0.2", commit="9e07f416a66b0ad304c720b61aa41cba9a0929d5")  # tag v3.0.2

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("rxn", default=False, description="Use inbuilt reaction code, useful with cray ftn")

    depends_on("mpi")
    depends_on("hdf5@1.8.12:+mpi+fortran+hl")
    depends_on("petsc@main:+hdf5+metis", when="@develop")
    depends_on("petsc@3.20:3.21+hdf5+metis", when="@5.0.0")
    depends_on("petsc@3.18:+hdf5+metis", when="@4.0.1")
    depends_on("petsc@3.16:+hdf5+metis", when="@3.0.2")

    # https://github.com/spack/spack/pull/37579#issuecomment-1545998141
    conflicts("^hdf5@1.14.1", when="%oneapi")

    def build(self, spec, prefix):
        if spec.satisfies("+rxn"):
            with working_dir("src/pflotran"):
                make("pflotran_rxn")
        else:
            make("all")

    def flag_handler(self, name, flags):
        if "%gcc@10:" in self.spec and name == "fflags":
            flags.append("-fallow-argument-mismatch")
        return flags, None, None

    @when("@5.0.0")
    def patch(self):
        filter_file(
            "use iso_[cC]_binding", "use, intrinsic :: iso_c_binding", "src/pflotran/hdf5_aux.F90"
        )
