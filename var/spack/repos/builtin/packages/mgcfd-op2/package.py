# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MgcfdOp2(MakefilePackage):
    """Package for the OP2 port of MGCFD: A 3D unstructured multigrid,
    finite-volume computational fluid dynamics (CFD) mini-app for inviscid-flow."""

    # NOTE: This package is new and has been tested on a limited set of use cases:
    # Graviton 2, Graviton 3:
    #       Compilers: GCC 12.1.0, Arm 22.0.1, NVHPC 22.3
    # ThunderX2 (Cray):
    #       Compilers: GCC 10.3.0, CCE 11.0.4

    homepage = "https://github.com/warwick-hpsc/MG-CFD-app-OP2"
    git = "https://github.com/warwick-hpsc/MG-CFD-app-OP2.git"

    maintainers("tomdeakin", "gihanmudalige", "bozbez")

    version("v1.0.0-rc1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")

    depends_on("gmake@4.3:")
    # KaHIP is a new MGCFD-OP2 dependency and
    # NVHPC builds require the latest develop branch at time of writing (Sept 22)
    depends_on("kahip@develop+metis", when="+mpi")
    depends_on("op2-dsl+mpi", when="+mpi")
    depends_on("op2-dsl~mpi", when="~mpi")

    def setup_build_environment(self, env):
        compiler_map = {"gcc": "gnu", "arm": "clang", "cce": "cray", "nvhpc": "pgi"}
        if self.spec.compiler.name in compiler_map:
            env.set("COMPILER", compiler_map[self.spec.compiler.name])
        else:
            env.set("COMPILER", self.spec.compiler.name)

        # Set Fortran compiler to GCC if using Arm.
        if self.spec.satisfies("%arm"):
            env.set("OP2_F_COMPILER", "gnu")

        # This overrides a flag issue in downstream OP2.
        if self.spec.satisfies("%nvhpc"):
            env.set("CFLAGS", "-O3 -DOMPI_SKIP_MPICXX -DMPICH_IGNORE_CXX_SEEK -DMPIPP_H")

    def edit(self, spec, prefix):
        # Makefile tweaks to ensure the correct compiler commands are called.
        makefile = FileFilter("Makefile")
        if self.spec.satisfies("%arm"):
            makefile.filter(r"CPP := clang", r"CPP := armclang")
            makefile.filter(r"-cxx=clang.*", "")

        if self.spec.satisfies("%nvhpc"):
            makefile.filter("pgc", "nvc")

    @property
    def build_targets(self):
        if "+mpi" in self.spec:
            builds = ["mpi", "mpi_vec", "mpi_openmp"]
            if "+cuda" in self.spec and spec.variants["cuda_arch"].value[0] != "none":
                builds.append("mpi_cuda")
        else:
            builds = ["seq", "openmp"]
            if "+cuda" in self.spec and spec.variants["cuda_arch"].value[0] != "none":
                builds.append("cuda")
        return builds

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("bin", prefix.bin)
