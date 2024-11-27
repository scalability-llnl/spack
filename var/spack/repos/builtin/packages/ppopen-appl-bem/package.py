# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PpopenApplBem(MakefilePackage):
    """ppOpen-APPL/BEM is software used to support a boundary element analysis
    executed on a parallel computer.

    The current version includes a software framework for a parallel BEM
    analysis and an H-matrix library.
    If you want to use the framework based on dense matrix computations,
    please move to the directory 'src/framework' and
    'src/framework_with_template'.
    If you want to use the H-matrix library, please
    move to the directly 'src/HACApK_with_BEM-BB-framework_1.0.0'.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    git = "https://github.com/Post-Peta-Crest/ppOpenHPC.git"

    version("master", branch="APPL/BEM")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    parallel = False
    hacapk_src_dir = join_path("HACApK_1.0.0", "src", "HACApK_with_BEM-BB-framework_1.0.0")
    src_directories = [
        join_path("bem-bb-framework_dense", "src", "framework_with_templates"),
        join_path("bem-bb-framework_dense", "src", "framework"),
        hacapk_src_dir,
    ]

    def edit(self, spec, prefix):
        flags = [self.compiler.openmp_flag]
        fflags = flags[:]
        if spec.satisfies("%gcc"):
            fflags.append("-ffree-line-length-none")
        filter_file(
            "bem-bb-SCM.out", "HACApK-bem-bb-sSCM.out", join_path(self.hacapk_src_dir, "Makefile")
        )
        for d in self.src_directories:
            with working_dir(d):
                with open("Makefile", "a") as m:
                    m.write("ifeq ($(SYSTEM),spack)\n")
                    m.write("    CC = {0}\n".format(spec["mpi"].mpicc))
                    m.write("    F90 = {0}\n".format(spec["mpi"].mpifc))
                    m.write("    CCFLAGS = {0}\n".format(" ".join(flags)))
                    m.write("    F90FLAGS = {0}\n".format(" ".join(fflags)))
                    m.write("    FFLAGS = {0}\n".format(" ".join(fflags)))
                    m.write("    LDFLAGS = {0}\n".format(" ".join(flags)))
                    m.write("endif\n")

    def build(self, spec, prefix):
        for d in self.src_directories:
            with working_dir(d):
                make("SYSTEM=spack")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.src)
        for d in self.src_directories:
            for f in find(d, "*.out"):
                copy(f, prefix.bin)
            install_src = join_path(prefix.src, os.path.basename(d))
            mkdir(install_src)
            install_tree(d, install_src)
            with working_dir(install_src):
                make("clean")
