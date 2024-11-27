# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PpopenApplAmrFdm(MakefilePackage):
    """
    ppOpen-APPL/AMR-FDM is an adaptive mesh refinement (AMR) framework
    for development of 3D parallel finite-difference method (FDM)
    applications.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/FDM_AMR")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    parallel = False
    build_targets = ["default", "advAMR3D"]

    def edit(self, spec, prefix):
        mkdirp("bin")
        mkdirp("lib")
        mkdirp("include")
        fflags = ["-O3", "-I."]
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter("^PREFIX +=.*", "PREFIX = {0}".format(prefix))
        makefile_in.filter("^INCDIR +=.*", "INCDIR = {0}/include".format(self.build_directory))
        makefile_in.filter("^LIBDIR +=.*", "LIBDIR = {0}/lib".format(self.build_directory))
        makefile_in.filter("^F90 +=.*", "F90 = {0}".format(spack_fc))
        makefile_in.filter("^MPIF90 +=.*", "MPIF90 = {0}".format(spec["mpi"].mpifc))
        makefile_in.filter("^sFFLAGS +=.*", "sFFLAGS = {0}".format(" ".join(fflags)))
        fflags.append(self.compiler.openmp_flag)
        makefile_in.filter("^pFFLAGS +=.*", "pFFLAGS = {0}".format(" ".join(fflags)))

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
        install_tree("lib", prefix.lib)
        install_tree("bin", prefix.bin)
        install_tree("doc", prefix.doc)
