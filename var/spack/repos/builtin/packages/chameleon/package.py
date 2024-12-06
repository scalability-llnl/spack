# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Chameleon(CMakePackage, CudaPackage):
    """Dense Linear Algebra for Scalable Multi-core Architectures and GPGPUs"""

    homepage = "https://gitlab.inria.fr/solverstack/chameleon"
    url = "https://gitlab.inria.fr/api/v4/projects/616/packages/generic/source/v1.2.0/chameleon-1.2.0.tar.gz"
    git = "https://gitlab.inria.fr/solverstack/chameleon.git"
    maintainers("fpruvost")

    version("master", branch="master", submodules=True)
    version("1.2.0", sha256="b8988ecbff19c603ae9f61441653c21bba18d040bee9bb83f7fc9077043e50b4")
    version("1.1.0", sha256="e64d0438dfaf5effb3740e53f3ab017d12744b85a138b2ef702a81df559126df")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # cmake's specific
    variant("shared", default=True, description="Build chameleon as a shared library")

    # chameleon's specific
    variant(
        "runtime",
        default="starpu",
        description="Runtime support",
        values=("openmp", "starpu"),
        multi=False,
    )
    variant("mpi", default=True, when="runtime=starpu", description="Enable MPI")
    variant("cuda", default=False, when="runtime=starpu", description="Enable CUDA")
    variant(
        "fxt",
        default=False,
        when="runtime=starpu",
        description="Enable FxT tracing support through StarPU",
    )
    variant(
        "simgrid",
        default=False,
        when="runtime=starpu",
        description="Enable simulation mode through StarPU+SimGrid",
    )

    # dependencies
    depends_on("pkgconfig", type="build")

    with when("runtime=starpu"):
        depends_on("starpu@1.3", when="@1.1.0")
        depends_on("starpu")
        depends_on("starpu~mpi", when="~mpi")
        depends_on("starpu+mpi", when="+mpi")
        depends_on("starpu~cuda", when="~cuda")
        depends_on("starpu+cuda", when="+cuda")
        with when("+simgrid"):
            depends_on("simgrid+msg")
            depends_on("starpu+simgrid")
            depends_on("starpu+mpi~shared+simgrid", when="+mpi")
            conflicts("^simgrid@:3.31", when="@:1.1.0")
            conflicts("+shared", when="+simgrid")
        with when("~simgrid"):
            depends_on("mpi", when="+mpi")
            depends_on("cuda", when="+cuda")
        with when("+fxt"):
            depends_on("fxt")
            depends_on("starpu+fxt")

    with when("~simgrid"):
        depends_on("blas")
        depends_on("lapack")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-Wno-dev",
            self.define("CMAKE_COLOR_MAKEFILE", "ON"),
            self.define("CMAKE_VERBOSE_MAKEFILE", "ON"),
            self.define("CHAMELEON_ENABLE_EXAMPLE", "ON"),
            self.define("CHAMELEON_ENABLE_TESTING", "ON"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CHAMELEON_USE_MPI", "mpi"),
            self.define_from_variant("CHAMELEON_USE_CUDA", "cuda"),
            self.define_from_variant("CHAMELEON_SIMULATION", "simgrid"),
        ]

        if spec.satisfies("runtime=openmp"):
            args.extend([self.define("CHAMELEON_SCHED", "OPENMP")])
        if spec.satisfies("runtime=starpu"):
            args.extend([self.define("CHAMELEON_SCHED", "STARPU")])

        if spec.satisfies("+mpi +simgrid"):
            args.extend(
                [
                    self.define("CMAKE_C_COMPILER", self.spec["simgrid"].smpicc),
                    self.define("CMAKE_CXX_COMPILER", self.spec["simgrid"].smpicxx),
                    self.define("CMAKE_Fortran_COMPILER", self.spec["simgrid"].smpifc),
                ]
            )

        if spec.satisfies("+mpi ~simgrid"):
            args.extend(
                [
                    self.define("MPI_C_COMPILER", self.spec["mpi"].mpicc),
                    self.define("MPI_CXX_COMPILER", self.spec["mpi"].mpicxx),
                    self.define("MPI_Fortran_COMPILER", self.spec["mpi"].mpifc),
                ]
            )

        if spec.satisfies("~simgrid"):
            if spec.satisfies("^intel-mkl") or spec.satisfies("^intel-parallel-studio+mkl"):
                if spec.satisfies("threads=none"):
                    args.extend([self.define("BLA_VENDOR", "Intel10_64lp_seq")])
                else:
                    args.extend([self.define("BLA_VENDOR", "Intel10_64lp")])
            elif spec.satisfies("^netlib-lapack"):
                args.extend([self.define("BLA_VENDOR", "Generic")])
            elif spec.satisfies("^openblas"):
                args.extend([self.define("BLA_VENDOR", "OpenBLAS")])

        return args
