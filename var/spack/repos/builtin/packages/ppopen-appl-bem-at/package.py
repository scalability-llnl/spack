# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PpopenApplBemAt(MakefilePackage):
    """
    ppOpen-APPL/BEM-AT is ppOpen-APPL/Bem with auto tuning.
    If you want to use ppOpen-APPL/BERM-AT, please copy files in
    src/framework_with_template from ppOpen-APPL/BEM install directory.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="ATA/BEM")

    depends_on("fortran", type="build")  # generated
    # In OAT_bem-bb-fw-dense-0.1.0.f90 the 2 variables are defined.
    # But ame variables are already defined in include file DAT.h.
    # This patch is deleted the variables definitions
    # in OAT_bem-bb-fw-dense-0.1.0.f90.
    patch("duplicate_defs.patch", when="@master")

    depends_on("mpi")
    depends_on("ppopen-appl-bem", type="run")

    parallel = False
    build_directory = "framework_with_templates"
    build_targets = ["SYSTEM=spack"]

    def edit(self, spec, prefix):
        flags = ["-O3", self.compiler.openmp_flag]
        fflags = flags[:]
        if spec.satisfies("%gcc"):
            fflags.append("-ffree-line-length-none")
        with open(join_path(self.build_directory, "Makefile"), "a") as m:
            m.write("ifeq ($(SYSTEM),spack)\n")
            m.write("    CC = {0}\n".format(spec["mpi"].mpicc))
            m.write("    F90 = {0}\n".format(spec["mpi"].mpifc))
            m.write("    CCFLAGS = {0}\n".format(" ".join(flags)))
            m.write("    F90FLAGS = {0}\n".format(" ".join(fflags)))
            m.write("    FFLAGS = {0}\n".format(" ".join(fflags)))
            m.write("    LDFLAGS = {0}\n".format(" ".join(flags)))
            m.write("endif\n")

    def install(self, spec, prefix):
        install_src_dir = join_path(prefix.src, self.build_directory)
        mkdir(prefix.bin)
        mkdirp(install_src_dir)
        for f in find(self.build_directory, "*.out"):
            copy(f, prefix.bin)
        install_src = join_path(prefix.src, self.build_directory)
        install_tree(self.build_directory, install_src_dir)
        with working_dir(install_src):
            make("clean")
