# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PpopenApplFvm(MakefilePackage):
    """
    ppOpen-APPL/FVM ia a coupling library that enables weak
    coupling on various simulation models, such as an
    atmospheric model and an ocean model, a seismic model
    and a structure model.  For getting very wide
    applicability, ppohMATHMP is designed so as that it is
    independent from grid structure.  Instead of grid
    structure, ppOpen-APPL/FVM requires a data set
    called 'mapping table'. Mapping table is composed of
    a correspondence table of grid indexes between a send
    model and a receive model and interpolation coefficients.
    A subroutine for making a mapping table file is provided
    by ppohMATHMP API.

    Current version of ppohMATHMP is ver.1.0 which targets
    scalar data exchange.  An exchange code of vector data
    which requires rotation calculation is under
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/FVM")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("metis@:4")

    def edit(self, spec, prefix):
        mkdirp("bin")
        mkdirp("lib")
        mkdirp("include")
        fflags = ["-O3"]
        if spec.satisfies("%gcc"):
            fflags.append("-ffree-line-length-none")
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter(r"^PREFIX *=.*$", "PREFIX = {0}".format(prefix))
        makefile_in.filter(r"^METISDIR *=.*$", "METISDIR = {0}".format(spec["metis"].prefix.lib))
        makefile_in.filter("mpifrtpx", spec["mpi"].mpifc)
        makefile_in.filter("frtpx", spack_fc)
        makefile_in.filter("-Kfast", " ".join(fflags))
        makefile_in.filter(",openmp", " {0}".format(self.compiler.openmp_flag))

        def install(self, spec, prefix):
            make("install")
            install_tree("examples", prefix.examples)
            install_tree("doc", prefix.doc)
