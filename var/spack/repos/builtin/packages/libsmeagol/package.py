# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsmeagol(MakefilePackage):
    """Non-equilibrium Green's function (NEGS) code."""

    homepage = "https://github.com/StefanoSanvitoGroup/libsmeagol"
    git = "https://github.com/StefanoSanvitoGroup/libsmeagol.git"

    maintainers("RMeli")

    license("GPL-2.0-or-later", checked_by="RMeli")

    version("main", branch="main")
    version("1.2", commit="fefed1bb4fceca584c3014debb169e8ed4ce1289")

    depends_on("mpi")
    depends_on("blas")

    def setup_build_environment(self, env):
        env.set("FCFLAGS", "-DMPI " + self.compiler.openmp_flag)

    @property
    def build_targets(self):
        spec = self.spec

        fcflags = "-DMPI -fopenmp -march=native -O3 -g -std=gnu -fallow-argument-mismatch -fexternal-blas -fblas-matmul-limit=0 -fno-omit-frame-pointer -funroll-loops"
        fixedform = "-ffixed-form"
        freeform = "-ffree-form -ffree-line-length-none"

        return [
            f"FC={spec['mpi'].mpifc}",
            f"FCFLAGS={fcflags} -fPIC",
            f"FCFLAGS_FIXEDFORM={fixedform}",
            f"FCFLAGS_FREEFORM={freeform}",
        ]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("obj", prefix.include)
