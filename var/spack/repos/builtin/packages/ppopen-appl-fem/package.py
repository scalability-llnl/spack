# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class PpopenApplFem(MakefilePackage):
    """
    ppOpen-APPL/FEM (ppohFEM) is a middleware to allow a Finite Element
    Method (FEM) analysis code developer to devote himself to development of
    the application software by offering a function commonly used in FEM.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/FEM")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("metis")

    # gcc does not support OpenMP atomic to same structure reference.
    # For example a%b = a%b - a%c
    # To avoid this, the patch is replace as follows:
    #   tmp = a%c
    #   !%omp atomic
    #   a%b = a%b - a%c
    patch("gcc_struct_atomic.patch", when="%gcc")
    parallel = False

    def edit(self, spec, prefix):
        fflags = ["-O3", "-I.", self.compiler.openmp_flag]
        if spec.satisfies("%gcc"):
            fflags.extend(["-cpp", "-ffree-line-length-none"])
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter(r"^PREFIX *=.*$", "PREFIX = {0}".format(prefix))
        makefile_in.filter(r"^F90OPTFLAGS *=.*$", "F90OPTFLAGS = {0}".format(" ".join(fflags)))
        makefile_in.filter(r"^METISDIR *=.*$", "METISDIR = {0}".format(spec["metis"].prefix))
        makefile_in.filter("mpicc", spec["mpi"].mpicc)
        makefile_in.filter("mpif90", spec["mpi"].mpifc)
        mkdirp(join_path("ppohFEM", "bin"))

    def install(self, spec, prefix):
        for d in ["ppohFEM", "app_flow", "app_heat", "app_struct"]:
            with working_dir(d):
                for install_dir in ["bin", "lib", "include"]:
                    if os.path.isdir(install_dir):
                        install_tree(install_dir, join_path(prefix, install_dir))
