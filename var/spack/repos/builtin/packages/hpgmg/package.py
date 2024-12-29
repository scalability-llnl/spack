# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hpgmg(MakefilePackage):
    """HPGMG implements full multigrid (FMG) algorithms using finite-volume and
    finite-element methods.

    Different algorithmic variants adjust the arithmetic intensity and architectural
    properties that are tested. These FMG methods converge up to discretization
    error in one F-cycle, thus may be considered direct solvers. An F-cycle visits
    the finest level a total of two times, the first coarsening (8x smaller) 4 times,
    the second coarsening 6 times, etc.
    """

    homepage = "https://bitbucket.org/hpgmg/hpgmg"
    url = "https://hpgmg.org/static/hpgmg-0.4.tar.gz"
    git = "https://bitbucket.org/hpgmg/hpgmg.git"

    tags = ["proxy-app"]

    license("BSD-2-Clause")

    version("develop", branch="master")
    version("0.4", sha256="abdabfe09453487299500b5bd8da4e6dc3d88477199bcfa38ac41d0b3c780f6f")
    version(
        "a0a5510df23b", sha256="b9c50f25e541428d4735fb07344d1d0ed9fc821bdde918d8e0defa78c0d9b4f9"
    )
    version("0.3", sha256="12a65da216fec91daea78594ae4b5a069c8f1a700f1ba21eed9f45a79a68c793")

    depends_on("c", type="build")  # generated

    variant("fe", default=False, description="Build finite element solver")
    variant(
        "fv",
        default="mpi",
        values=("serial", "mpi", "none"),
        description="Build finite volume solver with or without MPI support",
    )
    variant("cuda", default=False, description="Build with CUDA")
    variant("debug", default=False, description="Build in debug mode")

    depends_on("petsc", when="+fe")
    depends_on("mpi", when="+fe")
    depends_on("mpi", when="fv=mpi")
    depends_on("cuda", when="+cuda")
    depends_on("python", type="build")

    def configure_args(self):
        args = []
        if self.spec.satisfies("+fe") and not self.spec.satisfies("@0.3"):
            args.append("--fe")

        if self.spec.satisfies("fv=serial"):
            args.append("--no-fv-mpi")

        if self.spec.satisfies("^mpi"):
            args.append("--CC={0}".format(self.spec["mpi"].mpicc))

        cflags = []
        if self.spec.satisfies("fv=none"):
            args.append("--no-fv")
        else:
            # Apple's Clang doesn't support OpenMP
            if not self.spec.satisfies("%apple-clang"):
                cflags.append(self.compiler.openmp_flag)

        if self.spec.satisfies("+debug"):
            cflags.append("-g")
        else:
            cflags.append("-O3")

        args.append("--CFLAGS=" + " ".join(cflags))

        # Explicitly specify the build directory to ensure that
        # PETSC_ARCH is not used from the environment.
        args.append("--arch=build")

        return args

    def edit(self, spec, prefix):
        python("configure", *self.configure_args())

    def build(self, spec, prefix):
        make("-C", "build")

    def install(self, spec, prefix):
        install_tree("build/bin", prefix.bin)
        install("README.md", prefix)
        install("LICENSE", prefix)
