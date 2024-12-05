# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PpopenApplDemUtil(MakefilePackage):
    """
    ppOpen-APPL/DEM provides fundamental components of the particle
    simulations based on the discrete element method (DEM).
    ppOpen-APPL/DEM (ver.1.0.0) includes the libraries for the DEM,
    sample codes, and data sets. ppOpen-APPL/DEM-Util provides the
    preconditioning utilities. This utility prepares data sets of distributed
    data files from the mesh data sets.

    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/DEM")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def edit(self, spec, prefix):
        mkdirp("bin")
        mkdirp("lib")
        mkdirp("include")
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter("PREFIX += .*", "PREFIX = {0}".format(prefix))
        makefile_in.filter("F90 += .*", "F90 = {0}".format(spack_fc))
        makefile_in.filter("F77 += .*", "F77 = {0}".format(spack_fc))
        makefile_in.filter("MPIF90 += .*", "MPIF90 = {0}".format(spec["mpi"].mpifc))
        makefile_in.filter("MPIF77 += .*", "MPIF77 = {0}".format(spec["mpi"].mpifc))
        makefile_in.filter(
            "F90MPFLAGS += .*", "F90MPFLAGS = -O3 {0}".format(self.compiler.openmp_flag)
        )

    def install(self, spec, prefix):
        make("install")
        install_tree("doc", prefix.doc)
