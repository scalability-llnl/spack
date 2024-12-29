# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.build_environment import optimization_flags
from spack.package import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = "https://arbor-sim.org"
    git = "https://github.com/arbor-sim/arbor.git"
    url = "https://github.com/arbor-sim/arbor/releases/download/v0.8.1/arbor-v0.8.1-full.tar.gz"

    maintainers("thorstenhater", "brenthuisman")
    license("BSD-3-Clause")

    version("master", branch="master")
    version("develop")
    version(
        "0.9.0",
        sha256="5f9740955c821aca81e23298c17ad64f33f635756ad9b4a0c1444710f564306a",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.9.0/arbor-v0.9.0-full.tar.gz",
    )
    version(
        "0.8.1",
        sha256="caebf96676ace6a9c50436541c420ca4bb53f0639dcab825de6fa370aacf6baa",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.8.1/arbor-v0.8.1-full.tar.gz",
    )
    version(
        "0.8.0",
        sha256="18df5600308841616996a9de93b55a105be0f59692daa5febd3a65aae5bc2c5d",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.8/arbor-v0.8-full.tar.gz",
    )
    version(
        "0.7.0",
        sha256="c3a6b7193946aee882bb85f9c38beac74209842ee94e80840968997ba3b84543",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.7/arbor-v0.7-full.tar.gz",
    )
    version(
        "0.6.0",
        sha256="4cd333b18effc8833428ddc0b99e7dc976804771bc85da90034c272c7019e1e8",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.6/arbor-v0.6-full.tar.gz",
    )
    version(
        "0.5.2",
        sha256="290e2ad8ca8050db1791cabb6b431e7c0409c305af31b559e397e26b300a115d",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.5.2/arbor-v0.5.2-full.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("assertions", default=False, description="Enable arb_assert() assertions in code.")
    variant("doc", default=False, description="Build documentation.")
    variant("mpi", default=False, description="Enable MPI support")
    variant("python", default=True, description="Enable Python frontend support")
    variant(
        "vectorize", default=False, description="Enable vectorization of computational kernels"
    )
    variant(
        "gpu_rng",
        default=False,
        description="Use GPU generated random numbers -- not bitwise equal to CPU version",
        when="+cuda",
    )

    # https://docs.arbor-sim.org/en/latest/install/build_install.html#compilers
    conflicts("%gcc@:8")
    conflicts("%clang@:9")
    # Cray compiler v9.2 and later is Clang-based.
    conflicts("%cce@:9.1")
    conflicts("%intel")

    depends_on("cmake@3.19:", type="build")

    # misc dependencies
    depends_on("fmt@7.1:", when="@0.5.3:")  # required by the modcc compiler
    depends_on("fmt@9.1:", when="@0.7.1:")
    depends_on("googletest@1.12.1", when="@0.7.1:")
    depends_on("pugixml@1.11:", when="@0.7.1:")
    depends_on("nlohmann-json@3.11.2")
    depends_on("random123")
    with when("+cuda"):
        depends_on("cuda@10:")
        depends_on("cuda@11:", when="@0.7.1:")

    # mpi
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", when="+mpi+python", type=("build", "run"))

    # python (bindings)
    extends("python", when="+python")
    depends_on("python@3.7:", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    with when("+python"):
        depends_on("py-pybind11@2.6:", type="build")
        depends_on("py-pybind11@2.8.1:", when="@0.5.3:", type="build")
        depends_on("py-pybind11@2.10.1:", when="@0.7.1:", type="build")

    # sphinx based documentation
    depends_on("python@3.7:", when="+doc", type="build")
    depends_on("py-sphinx", when="+doc", type="build")
    depends_on("py-svgwrite", when="+doc", type="build")

    @property
    def build_targets(self):
        return ["all", "html"] if "+doc" in self.spec else ["all"]

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("ARB_WITH_ASSERTIONS", "assertions"),
            self.define_from_variant("ARB_WITH_MPI", "mpi"),
            self.define_from_variant("ARB_WITH_PYTHON", "python"),
            self.define_from_variant("ARB_VECTORIZE", "vectorize"),
            self.define("ARB_ARCH", "none"),
            self.define("ARB_CXX_FLAGS_TARGET", optimization_flags(self.compiler, spec.target)),
        ]

        if self.spec.satisfies("+cuda"):
            args.extend(
                [
                    self.define("ARB_GPU", "cuda"),
                    self.define_from_variant("ARB_USE_GPU_RNG", "gpu_rng"),
                ]
            )

        return args

    @run_after("install", when="+python")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python("-c", "import arbor")
