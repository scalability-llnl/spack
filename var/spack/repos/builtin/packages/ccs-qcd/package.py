# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.error import SpackError
from spack.package import *


def class_validator(values):
    """1, 2, 3, 4, 5, 6"""
    values = int(values[0])
    if values < 1 or values > 6:
        error_msg = (
            "class: Choose one of the following:\n"
            "1  - 8x8x8x32 (default MPI config: 1x1x1)\n"
            "2  - 32x32x32x32 (default MPI config: 4x4x4)\n"
            "3  - 64x64x64x32 (default MPI config: 8x8x8)\n"
            "4  - 160x160x160x160 (default MPI config: 20x20x20)\n"
            "5  - 256x256x256x256 (default MPI config: 32x32x32)\n"
            "6  - 192x192x192x192 (default MPI config: 24x24x24)"
        )
        raise SpackError(error_msg)


class CcsQcd(MakefilePackage):
    """This program benchmarks the performance of a linear equation solver
    with a large sparse coefficient matrix appering in a lattice QCD
    probrem. Lattice QCD describes the property of protons, neutrons and
    neucleons in terms of more fundamental interacting elementary particles
    gluon and quarks."""

    homepage = "https://github.com/fiber-miniapp/ccs-qcd"
    git = "https://github.com/fiber-miniapp/ccs-qcd.git"

    tags = ["hep"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.2.1", commit="d7c6b6923f35a824e997ba8db5bd12dc20dda45c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "class",
        default=1,
        values=class_validator,
        description="This miniapp has five problem classes, for which the"
        " first three are relatively small problems just for testing"
        " this miniapp itself. The remaining two are the target problem"
        " sizes for the HPCI FS evaluation.",
        multi=False,
    )

    depends_on("mpi")

    parallel = False

    def edit(self, spec, prefix):
        if spec.satisfies("%gcc") and spec.satisfies("arch=aarch64:"):
            chgopt = (
                "FFLAGS  =-O3 -ffixed-line-length-132 -g -fopenmp" " -mcmodel=large -funderscoring"
            )
            filter_file(
                "FFLAGS  =.*",
                chgopt,
                join_path(self.stage.source_path, "src", "make.gfortran.inc"),
            )
        if spec.satisfies("%fj"):
            filter_file(
                "mpifrtpx",
                spec["mpi"].mpifc,
                join_path(self.stage.source_path, "src", "make.fx10.inc"),
            )
            filter_file(
                "mpifccpx",
                spec["mpi"].mpicc,
                join_path(self.stage.source_path, "src", "make.fx10.inc"),
            )
        else:
            filter_file(
                "mpif90",
                spec["mpi"].mpifc,
                join_path(self.stage.source_path, "src", "make.gfortran.inc"),
            )
            filter_file(
                "mpicc",
                spec["mpi"].mpicc,
                join_path(self.stage.source_path, "src", "make.gfortran.inc"),
            )

    def build(self, spec, prefix):
        ccs_class = "CLASS=" + spec.variants["class"].value
        with working_dir("src"):
            if spec.satisfies("%fj"):
                make("MAKE_INC=make.fx10.inc", ccs_class)
            else:
                make("MAKE_INC=make.gfortran.inc", ccs_class)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("./src/ccs_qcd_solver_bench_class" + spec.variants["class"].value, prefix.bin)
