# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack.package import *


class OmmBundle(MakefilePackage):
    """Omm-bundle is a library implementing the orbital minimization method for
    solving the Kohn-Sham equation as a generalized eigenvalue problem and
    a bundle of four separate libraries: pspBLAS, MatrixSwitch, libOMM, tomato."""

    homepage = "https://esl.cecam.org/"
    git = "https://gitlab.com/ElectronicStructureLibrary/omm/omm-bundle.git"

    version("master", branch="master")
    version("1.0.0", tag="v1.0.0", commit="8b644267284695ff1a40b78d098bda6464a7b821")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("dbcsr")

    # Avoid duplicate include error in mpi.h in Fujitsu compiler
    patch("fjmpi_pspBasicTool.patch", when="@: %fj")

    def edit(self, spec, prefix):
        # edit make.inc
        shutil.copy("make.inc.example", "make.inc")
        makeinc = FileFilter("make.inc")
        makeinc.filter("FORTRAN   =.*", "FORTRAN   = {0}".format(spec["mpi"].mpifc))
        linalg_libs = (
            self.spec["lapack"].libs + self.spec["blas"].libs + self.spec["scalapack"].libs
        )
        makeinc.filter("LINALG_LIBS =.*", "LINALG_LIBS = {0}".format(linalg_libs.ld_flags))
        makeinc.filter("#FPPFLAGS ", "FPPFLAGS ")
        makeinc.filter("#DBCSR     =.*", "DBCSR = {0}".format(spec["dbcsr"].prefix))
        makeinc.filter("#DBCSRINC ", "DBCSRINC ")
        makeinc.filter("#DBCSRLIB  =.*", "DBCSRLIB = -L$(DBCSR)/lib64 -ldbcsr")

        # fix Makefile of tomato to avoid error(cp: cannot stat '*.mod': No such file or directory)
        tomato_makefile = FileFilter("tomato/src/Makefile.manual")
        tomato_makefile.filter("	cp *.mod $(BUILDPATH)/include; \\\n", "")

    def build(self, spec, prefix):
        make("-f", "Makefile.manual", "all", parallel=False)

    def install(self, spec, prefix):
        for d in ["pspBLAS", "MatrixSwitch", "libOMM", "tomato"]:
            install_tree("build_" + d, prefix + "/build_" + d)
