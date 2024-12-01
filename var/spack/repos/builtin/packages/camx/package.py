# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Camx(MakefilePackage):
    """Comprehensive Air Quality Model with Extensions."""

    homepage = "https://www.camx.com"
    # Upstream obfuscates their download URL to get you to fill out their
    # registration form and accept their license agreement.

    version(
        "6.50",
        url="https://www.camx.com/getmedia/caaf7983-616b-4207-bd10-c2b404bda78d/CAMx_v6-50-src-180430.tgz",
        sha256="4a53f78e0722d85a9c7d8ed6732aff55163a4ce06f69b6bbc9e00a3bf36a756c",
    )
    resource(
        when="@6.50",
        name="user_manual",
        url="https://www.camx.com/files/camxusersguide_v6-50.pdf",
        sha256="b02d9826d59f22f9daa5955bb7b9fd3e0ca86eb73017c5845896d40391c64588",
        expand=False,
        placement="doc",
    )
    resource(
        when="@6.50",
        name="input_data",
        url="https://www.camx.com/getmedia/77ad8028-9388-4f5d-bcab-a418e15dde68/v6-50-specific-inputs-180430.tgz",
        sha256="89b58283e37b8e2bd550a8ec62208f241be72c78dc26da9c42ad63c34f54ebfb",
        placement="data",
    )

    variant("mpi", default=True, description="Enable MPI")
    variant(
        "threads",
        default="pthread",
        description="Multithreading support",
        values=("pthread", "openmp"),
        multi=False,
    )

    depends_on("mpi", when="+mpi")

    parallel = False

    def patch(self):
        # Relax values in parameter file to fix fun errors like this:
        #
        # ERROR in STARTUP:
        #  A parameter in the camx.prm is not sufficiently large.
        #  Please change the value for parameter: MXCELLS
        #  It should be set to a value of at least:          396
        with working_dir("Includes"):
            duplicate = "camx.prm"
            os.remove(duplicate)
            orig = "camx.prm.v{0}".format(self.spec.version)
            prm = FileFilter(orig)
            prm.filter(r"MXCELLS = [^)]+", "MXCELLS = 400 ")
            prm.filter(r"MXPTSRC = [^)]+", "MXPTSRC = 1355961 ")
            prm.filter(r"MXLAYER = [^)]+", "MXLAYER = 40 ")
            prm.filter(r"MXPIG = [^)]+", "MXPIG = 100000 ")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        if spec.target.family == "aarch64":
            makefile.filter("-mcmodel=medium", "-mcmodel=large")
            makefile = FileFilter("./MPI/util/Makefile")
            makefile.filter("-mcmodel=medium", "-mcmodel=large")

        # Support Intel MPI.
        if spec["mpi"].name == "intel-mpi":
            makefile.filter(
                "else ifneq (, $(findstring $(MPI),openmpi openMPI OPENMPI))",
                """else ifneq (, $(findstring $(MPI),intel-mpi intel impi))
    MPI_ECHO = "* MPI will be built in using Intel MPI"
    MPI_INC = $(MPI_INST)/include
    MPI_LIBS = -L$(CAMX_MPI)/util -lutil -lparlib """
                + spec["mpi"].libs.ld_flags
                + """
    MPI_STRING = IntelMPI
    FC = $(MPI_INST)/bin64/mpifort
    CC = $(MPI_INST)/bin64/mpicc
else ifneq (, $(findstring $(MPI),openmpi openMPI OPENMPI))""",
                string=True,
            )
            makefile.filter("OPENMPI MVAPICH", "OPENMPI MVAPICH IntelMPI", string=True)

        if spec.satisfies("+mpi"):
            # Substitute CC, FC.
            makefile.filter("CC = .*", "CC = " + spec["mpi"].mpicc)
            makefile.filter("FC = .*", "FC = " + spec["mpi"].mpifc)
            # Fix parlib not being compiled.
            makefile.filter(
                "all: comp_$(COMPILER)",
                # Yes, flake8, Makefile rules needs tabs!
                """all: parlib comp_$(COMPILER)
parlib :
	$(MAKE) -C $(CAMX_MPI)/util  # noqa: E101,W191
""",
                string=True,
            )  # noqa: E101
            makefile_parlib = FileFilter("MPI/util/Makefile")
            makefile_parlib.filter("CC = .*", "CC = " + spec["mpi"].mpicc)
            makefile_parlib.filter("LIBS = .*", "LIBS = " + spec["mpi"].libs.ld_flags)
            makefile_parlib.filter("MPI_INST = .*", "MPI_INST = " + spec["mpi"].prefix)
        else:
            # Substitute CC, FC.
            makefile.filter("CC = .*", "CC = " + env["CC"])
            makefile.filter("FC = .*", "FC = " + env["FC"])

    @property
    def build_targets(self):
        # Set compiler.
        omp = ["", "omp"][self.spec.satisfies("threads=openmp")]
        compiler = os.path.basename(env["FC"]) + omp
        args = ["COMPILER={0}".format(compiler)]
        # Set MPI.
        if self.spec.satisfies("+mpi"):
            mpi = self.spec["mpi"]
            args += ["MPI={0}".format(mpi.name), "MPI_INST={0}".format(mpi.prefix)]
        return args

    def install(self, spec, prefix):
        exe = glob.glob("CAMx.*")[0]
        mkdir(prefix.bin)
        install(exe, prefix.bin.camx)
        mkdirp(prefix.share.doc)
        install_tree("doc", prefix.share.doc, symlinks=False)
        mkdir(prefix.share.data)
        install_tree("data", prefix.share.data)
