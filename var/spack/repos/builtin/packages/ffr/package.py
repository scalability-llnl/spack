# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ffr(MakefilePackage):
    """FFR: FrontFlow/red, developed in Frontier Simulation Software
    for Industrial Science(FSIS) project supported by IT program of
    Ministry of Education, Culture, Sports, Science and Technology(MEXT),
    JAPAN."""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/rss21/theme/multi/fluid/fluid_softwareinfo.html"
    manual_download = True

    version(
        "3.1.004",
        sha256="2b396f66bb6437366721fac987f9c6e8b830638c3e4cb5df6a08ff41633f8481",
        url="file://{0}/FFR_V3.1.004.zip".format(os.getcwd()),
    )
    version(
        "3.0_000",
        sha256="edc69fb1fd9dbdb3f531a8f2b9533a9b3c1a28768bb4029b84a6b35c95db0b48",
        url="file://{0}/open_FrontFlowRed_3.0_000.tar.gz".format(os.getcwd()),
    )

    # FrontFlow/red used Fortran format I/E without width (For Example 3I)
    # But gfortran require width (For Example (3I6).
    patch("gfortran_format_31.patch", when="@3.1.004 %gcc")
    patch("gfortran_format_30.patch", when="@3.0_000 %gcc")

    depends_on("mpi")
    depends_on("metis@:4", type="link")

    parallel = False
    build_directories = [
        join_path("src_main", "src"),
        join_path("src_pre", "src"),
        join_path("FFR2VIZ", "src"),
        join_path("FFR2VIZ", "src_P_for"),
    ]

    def edit(self, spec, prefix):
        flags = ["-O3", "-I.", "-I{0}".format(spec["metis"].prefix.include)]
        fflags = flags[:]
        if spec.satisfies("%gcc"):
            fflags.append("-ffixed-line-length-none")
        elif spec.satisfies("%fj"):
            fflags.append("-Fwide")
        d = find(".", "src_main", recursive=True)
        src_main = d[0]
        root_dir = os.path.dirname(src_main)
        make = join_path(root_dir, "src_pre", "src", "Makefile")
        os.chmod(make, 0o644)
        filter_file("#CSRCS =.*$", "CSRCS = kmetis_main.c io.c", make)
        filter_file("LIBPRE =.*$", "LIBPRE = " + spec["metis"].libs.ld_flags, make)

        make = join_path(src_main, "src", "Makefile")
        os.chmod(make, 0o644)
        with open(make, "a") as m:
            m.write("module_hpc.o: module_hpc.f\n")
            m.write("\t$(MPI_F90) $(FFLAGS) -c $<\n")
            m.write("\n")
            m.write("hpc.o: hpc.f\n")
            m.write("\t$(MPI_F90) $(FFLAGS) -c $<\n")

        if spec.satisfies("@3.0_000"):
            for d in ["src_pre", "FFR2VIZ"]:
                workdir = join_path(root_dir, d, "src")
                make = join_path(workdir, "Makefile")
                os.chmod(make, 0o644)
                m = FileFilter(make)
                m.filter(r"include Makefile\..*\.in", "include Makefile.spack.in")
                with open(join_path(workdir, "Makefile.spack.in"), "w") as m:
                    m.write("OS = {0}\n".format(spec.os))
                    m.write("F90 = {0}\n".format(spack_fc))
                    m.write("F90LINKER = {0}\n".format(spack_fc))
                    m.write("FOPTIONS = {0}\n".format(" ".join(fflags)))
                    m.write("CC = {0}\n".format(spack_cc))
                    m.write("COPTIONS = {0}\n".format(" ".join(flags)))
                    m.write("MPI_HOME = \n")
                    m.write("MPI_INCLUDE = \n")
                    m.write("MPI_LIBS = ")
                    m.write("MPI_F90 = {0} {1}\n".format(spec["mpi"].mpifc, " ".join(fflags)))
                    m.write("AR = ar rv\n")
                    m.write("RANLIB = :\n")
        for makefile_in in find(".", "Makefile.in", recursive=True):
            os.chmod(makefile_in, 0o644)
            m = FileFilter(makefile_in)
            m.filter(r"OS\s*=.*$", "OS = {0}".format(spec.os))
            m.filter(r"F90\s*=.*$", "F90 = {0}".format(spack_fc))
            m.filter(r"F90LINKER\s*=.*$", "F90LINKER = {0}".format(spack_fc))
            m.filter(r"FOPTIONS\s+=.*$", "FOPTIONS = {0}".format(" ".join(fflags)))
            m.filter(r"CC\s+=.*$", "CC = {0}".format(spack_cc))
            m.filter(r"COPTIONS\s+=.*$", "COPTIONS = {0}".format(" ".join(flags)))
            m.filter(r"MPI_HOME\s+=.*$", "MPI_HOME = ")
            m.filter(r"MPI_INC\s+=.*$", "MPI_INCLUDE = ")
            m.filter(r"MPI_LIBS\s+=.*$", "MPI_LIBS = ")
            m.filter(
                r"MPI_F90\s+=.*$", "MPI_F90 = {0} {1}".format(spec["mpi"].mpifc, " ".join(fflags))
            )
            m.filter(r"AR\s+=.*$", "AR = ar rv")
            m.filter(r"RANLIB =.*$", "RANLIB = :")

    def build(self, spec, prefix):
        d = find(".", "src_main", recursive=True)
        root_dir = os.path.dirname(d[0])
        copy(
            join_path(root_dir, "src_metis_4.1_fflow", "Lib", "kmetis_main.c"),
            join_path(root_dir, "src_pre", "src"),
        )
        copy(
            join_path(root_dir, "src_metis_4.1_fflow", "Lib", "io.c"),
            join_path(root_dir, "src_pre", "src"),
        )
        mkdirp(join_path(root_dir, "bin_FFR"))
        for dir in self.build_directories:
            with working_dir(join_path(root_dir, dir)):
                make("clean")
                make()

    def install(self, spec, prefix):
        d = find(".", "src_main", recursive=True)
        root_dir = os.path.dirname(d[0])
        install_tree(join_path(root_dir, "bin_FFR"), prefix.bin)
