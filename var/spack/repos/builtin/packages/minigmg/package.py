# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Minigmg(Package):
    """miniGMG is a compact benchmark for understanding the performance
    challenges associated with geometric multigrid solvers
    found in applications built from AMR MG frameworks
    like CHOMBO or BoxLib when running
    on modern multi- and manycore-based supercomputers.
    It includes both productive reference examples as well as
    highly-optimized implementations for CPUs and GPUs.
    It is sufficiently general that it has been used to evaluate
    a broad range of research topics including PGAS programming models
    and algorithmic tradeoffs inherit in multigrid. miniGMG was developed
    under the CACHE Joint Math-CS Institute.

    Note, miniGMG code has been supersceded by HPGMG."""

    homepage = (
        "https://crd.lbl.gov/departments/computer-science/PAR/research/previous-projects/miniGMG/"
    )
    url = "https://crd.lbl.gov/assets/Uploads/FTG/Projects/miniGMG/miniGMG.tar.gz"

    license("BSD-3-Clause-LBNL")

    version("master", sha256="1c2d27496a881f655f5e849d6a7a132625e535739f82575991c511cc2cf899ac")

    depends_on("c", type="build")  # generated

    variant(
        "vec",
        default="ompif",
        description="Which method of vectorisation to use",
        values=("ompif", "sse", "avx", "simde"),
        multi=False,
    )

    variant("opt", default=False, description="Enable optimization flags for improved OpenMP")

    depends_on("mpi")

    # Set up SIMD Everywhere config
    depends_on("simde", when="vec=simde")
    patch("simde.patch", when="vec=simde")

    # Patch to add timer for Aarch64 rather than rdtsc
    patch("aarch64_time.patch", when="target=aarch64:")

    # Replaces inline with inline static, for correct syntax
    patch("inline_static.patch")

    def install(self, spec, prefix):
        cc = Executable(spec["mpi"].mpicc)

        args = []

        # Default optimisation level
        if spec.satisfies("+opt"):
            if self.spec.satisfies("%nvhpc"):
                args.append("-fast")
            else:
                args.append("-Ofast")
        else:
            args.append("-O3")

        # Add OpenMP flag
        args += [self.compiler.openmp_flag]

        args += ["miniGMG.c", "mg.c", "box.c", "solver.c"]

        # Set the correct operators file - using the vec variant
        if spec.satisfies("vec=sse"):
            args += ["operators.sse.c"]
        elif spec.satisfies("vec=avx"):
            args += ["operators.avx.c"]
        elif spec.satisfies("vec=simde"):
            args += ["operators.simde.c"]
        else:
            args += ["operators.ompif.c"]

        # Switch out timer file (depends on patch)
        if spec.satisfies("target=aarch64:"):
            args += ["timer.aarch64.c"]
        else:
            args += ["timer.x86.c"]

        args += ["-D__MPI"]

        if spec.satisfies("+opt"):
            args += ["-D__PREFETCH_NEXT_PLANE_FROM_DRAM"]
            args += ["-D__FUSION_RESIDUAL_RESTRICTION"]
        else:
            args += ["-D__COLLABORATIVE_THREADING=6"]

        args += ["-D__TEST_MG_CONVERGENCE", "-D__PRINT_NORM", "-D__USE_BICGSTAB"]
        args += ["-o", "run.miniGMG", "-lm"]

        cc(*args)

        mkdir(prefix.bin)
        install("run.miniGMG", prefix.bin)
        mkdir(prefix.jobs)
        install("job*", prefix.jobs)
