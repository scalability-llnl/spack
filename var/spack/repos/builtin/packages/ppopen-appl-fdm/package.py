# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PpopenApplFdm(MakefilePackage):
    """
    ppOpen-APPL/FDM is a application software for the FDM simulation of
    seismic wave propagation in elastic media in 2D and 3D.
    The 2D application is prepared for a single-CPU (sequential) calculation
    and the 3D application use MPI and OpenMP for parallel computing.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/FDM")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # remove unused variable definition
    patch("unused.patch")
    # remove iargc external definition
    # iargc is intrinsic in gfortran
    patch("gfortran_iargc.patch", when="%gcc")

    # Fixed a problem that 'iargc' was not declared in advance
    patch("iargc_definition.patch", when="%fj")

    depends_on("ppopen-math-vis", type="link")
    depends_on("mpi")

    parallel = False

    def edit(self, spec, prefix):
        makefile_in = FileFilter("Makefile.in")
        makefile_in.filter("PREFIX += .*$", "PREFIX = {0}".format(prefix))
        makefile_in.filter("LIBDIR = .*$", "LIBDIR = {0}".format(prefix))
        makefile_in.filter("CC += .*$", "CC = {0}".format(spec["mpi"].mpicc))
        makefile_in.filter("COPTFLAGS += .*$", "COPTFLAGS = -O3")
        makefile_in.filter("CXX += .*$", "CXX = {0}".format(spec["mpi"].mpicxx))
        makefile_in.filter("CXXOPTFLAGS = .*$", "CXXOPTFLAGS = -O3")
        makefile_in.filter("FC += .*$", "FC = {0}".format(spec["mpi"].mpifc))
        makefile_in.filter("FOPTFLAGS += .*$", "FOPTFLAGS = -O3")
        makefile_in.filter("F90 += .*$", "F90 = {0}".format(spec["mpi"].mpifc))
        makefile_in.filter("F90OPTFLAGS += .*$", "F90OPTFLAGS = -O3")

        makefile_opt = FileFilter(join_path("src", "seismic_2D", "makefile.option"))
        makefile_opt.filter("FC = .*$", "FC = {0}".format(spack_fc))
        makefile_opt.filter("FFLAGS = .*$", "FFLAGS = -O3")

        makefile = FileFilter(join_path("src", "seismic_3D", "1.ppohFDM-ppohVIS", "Makefile"))
        makefile.filter("LIBS += .*$", "LIBS = ")
        makefile.filter("FLDFLAGS += .*$", "FLDFLAGS = " + spec["ppopen-math-vis"].libs.ld_flags)

        makefile_opt = FileFilter(join_path("src", "seismic_3D", "3.parallel", "Makefile.option"))
        makefile_opt.filter("FC = .*$", "FC = {0}".format(spec["mpi"].mpifc))
        makefile_opt.filter("FFLAGS = .*$", "FFLAGS = -O3 {0}".format(self.compiler.openmp_flag))

        copy(
            join_path("examples", "seismic_3D-example", "m_param.f90"),
            join_path("src", "seismic_3D", "1.ppohFDM-ppohVIS"),
        )
        copy(
            join_path("examples", "seismic_3D-example", "m_param.f90"),
            join_path("src", "seismic_3D", "3.parallel"),
        )

        for makefile in find("tools", "makefile", recursive=True):
            fflags = ["-O3", "-I."]
            m = FileFilter(makefile)
            m.filter("^FC =.*$", "FC = {0}".format(spack_fc))
            m.filter("^FFLAGS =.*$", "FFLAGS = {0}".format(" ".join(fflags)))

    def build(self, spec, prefix):
        make("seism2d", "seism3d-ppohVIS", "seism3d-parallel")
        for d in ["seismic_2D-tools", "seismic_3D-tools"]:
            with working_dir(join_path("tools", d)):
                make("all")

    def install(self, spec, prefix):
        commands = [
            join_path("src", "seismic_2D", "seism2d_psv"),
            join_path("src", "seismic_3D", "3.parallel", "seism3d3n"),
            join_path("src", "seismic_3D", "1.ppohFDM-ppohVIS", "seism3d3n"),
            join_path("tools", "seismic_2D-tools", "pmxy2d"),
            join_path("tools", "seismic_2D-tools", "rwav2d"),
            join_path("tools", "seismic_3D-tools", "catsnap"),
            join_path("tools", "seismic_3D-tools", "catwav"),
            join_path("tools", "seismic_3D-tools", "ppmxy3d3"),
            join_path("tools", "seismic_3D-tools", "rwav3d"),
        ]
        mkdir(prefix.bin)
        for command in commands:
            copy(command, prefix.bin)
        install_tree("examples", prefix.examples)
        install_tree("doc", prefix.doc)
        install_tree("src", prefix.src)
        copy("Makefile.in", prefix)
        clean_dir = [
            join_path(prefix.src, "seismic_2D"),
            join_path(prefix.src, "seismic_3D", "1.ppohFDM-ppohVIS"),
            join_path(prefix.src, "seismic_3D", "3.parallel"),
        ]
        for d in clean_dir:
            with working_dir(d):
                make("clean")
        force_remove(join_path(prefix, "Makefile.in"))
