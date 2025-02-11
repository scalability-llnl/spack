# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = "https://arbor-sim.org"
    git = "https://github.com/arbor-sim/arbor.git"
    url = "https://github.com/arbor-sim/arbor/releases/download/v0.8.1/arbor-v0.10.0-full.tar.gz"
    maintainers = ("thorstenhater", "boeschf")
    license("BSD-3-Clause")

    version("master", branch="master")
    version("develop")
    version(
        "0.10.0",
        sha256="72966b7a2f45ce259b8ba167ca3e4f5ab9f212136a300267aaac0c04ed3fe3fc",
        url="https://github.com/arbor-sim/arbor/releases/download/v0.10.1/arbor-v0.10.0-full.tar.gz",
    )
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
    variant("hwloc", default=False, description="support for thread pinning via HWLOC")
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
    depends_on("fmt@10.2:", when="@0.9.1:")
    depends_on("fmt@10.2:", when="@0.10.0:")
    depends_on("googletest@1.12.1:", when="@0.7.1:")
    depends_on("pugixml@1.11:", when="@0.7.1:")
    depends_on("pugixml@1.13:", when="@0.9.1:")
    depends_on("pugixml@1.14:", when="@0.10.0:")
    depends_on("nlohmann-json@3.11.3:")
    depends_on("random123@1.14.0:")
    with when("+cuda"):
        depends_on("cuda@10:")
        depends_on("cuda@11:", when="@0.7.1:")
        depends_on("cuda@12:", when="@0.9.1:")
        depends_on("cuda@12:", when="@0.10.0:")

    # mpi
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", when="+mpi+python", type=("build", "run"))

    # hwloc
    depends_on("hwloc@2:", when="+hwloc", type=("build", "run"))

    # python (bindings)
    with when("+python"):
        extends("python")
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("python@3.9:", when="@0.9.1:", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-pybind11@2.6:", type="build")
        depends_on("py-pybind11@2.8.1:", when="@0.5.3:", type="build")
        depends_on("py-pybind11@2.10.1:", when="@0.7.1:", type="build")
        depends_on("py-pybind11@2.10.1:", when="@0.7.1:", type="build")
        depends_on("py-pybind11@2.10.1:", when="@2.11.1:", type="build")

    # sphinx based documentation
    with when("+doc"):
        depends_on("python@3.10:", type="build")
        depends_on("py-sphinx", type="build")
        depends_on("py-svgwrite", type="build")

    @property
    def build_targets(self):
        return ["all", "html"] if "+doc" in self.spec else ["all"]

    def cmake_args(self):
        args = [
            self.define_from_variant("ARB_WITH_ASSERTIONS", "assertions"),
            self.define_from_variant("ARB_WITH_MPI", "mpi"),
            self.define_from_variant("ARB_WITH_PYTHON", "python"),
            self.define_from_variant("ARB_VECTORIZE", "vectorize"),
            self.define_from_variant("ARB_USE_HWLOC", "hwloc"),
        ]

        if "+cuda" in self.spec:
            args.append("-DARB_GPU=cuda")
            args.append(self.define_from_variant("ARB_USE_GPU_RNG", "gpu_rng"))

        # query spack for the architecture-specific compiler flags set by its wrapper
        args.append("-DARB_ARCH=none")
        opt_flags = self.spec.target.optimization_flags(
            self.spec.compiler.name, str(self.spec.compiler.version)
        )
        # Might return nothing
        if opt_flags:
            args.append("-DARB_CXX_FLAGS_TARGET=" + opt_flags)
        return args

    @run_after("install", when="+python")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python("-c", "import arbor")
