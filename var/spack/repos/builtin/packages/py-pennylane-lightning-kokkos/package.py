# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.cmake
from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyPennylaneLightningKokkos(CMakePackage, PythonExtension, CudaPackage, ROCmPackage):
    """The PennyLane-Lightning-Kokkos plugin provides
    a fast state-vector simulator with Kokkos kernels."""

    homepage = "https://docs.pennylane.ai/projects/lightning-kokkos"
    git = "https://github.com/PennyLaneAI/pennylane-lightning-kokkos.git"

    maintainers("AmintorDusko", "vincentmr")

    license("Apache-2.0")

    version("main", branch="main")
    version("master", branch="master")
    version("0.37.0", sha256="3f70e3e3b7e4d0f6a679919c0c83e451e129666b021bb529dd02eb915d0666a0")
    version("0.36.0", sha256="c5fb24bdaf2ebdeaf614bfb3a8bcc07ee83c2c7251a3893399bb0c189d2d1d01")
    version("0.35.1", sha256="d39a2749d08ef2ba336ed2d6f77b3bd5f6d1b25292263a41b97943ae7538b7da")
    version("0.35.0", sha256="1a16fd3dbf03788e4f8dd510bbb668e7a7073ca62be4d9414e2c32e0166e8bda")
    version("0.34.0", sha256="398c3a1d4450a9f3e146204c22329da9adc3f83a1685ae69187f3b25f47824c0")
    version("0.33.1", sha256="878f63cd1afadd52386b1aca9c0e3fb0a097b64ce8e347b325ebc7cac722e5e0")
    version("0.33.0", sha256="c4cab4a8a1a53edc0990a2a429805dca1c6a46a7ffcc6f77c985b88cd6ff6247")
    version("0.32.0", sha256="06f19dfb1073387ef9ee30c38ea44884844a771373256b694a0e1ceb87195bb2")
    version("0.31.0", sha256="fe10322fee0fa7df45cd3a81d6c229a79c7dfa7f20ff7d67c65c9a28f494dc89")
    version("0.30.0", sha256="7c8f0e0431f8052993cd8033a316f53590c7bf5419445d0725e214b93cbc661b")
    version("0.29.1", sha256="f51ba7718defc7bb5064f690f381e04b2ec58cb09f22a171ae5f410860716e30")

    depends_on("cxx", type="build")  # generated

    depends_on("kokkos@:3.7.2", when="@:0.30", type=("run", "build"))
    depends_on("kokkos@4:4.1", when="@0.31", type=("run", "build"))
    depends_on("kokkos@4:4.2", when="@0.32:0.36", type=("run", "build"))
    depends_on("kokkos@4.3:", when="@0.37:", type=("run", "build"))

    # kokkos backends
    backends = {
        "cuda": [False, "Whether to build CUDA backend"],
        "openmp": [False, "Whether to build OpenMP backend"],
        "openmptarget": [False, "Whether to build the OpenMPTarget backend"],
        "threads": [False, "Whether to build the C++ threads backend"],
        "rocm": [False, "Whether to build HIP backend"],
        "serial": [True, "Whether to build serial backend"],
        "sycl": [False, "Whether to build the SYCL backend"],
    }

    for backend in backends:
        deflt_bool, descr = backends[backend]
        variant(backend.lower(), default=deflt_bool, description=descr)
        depends_on(f"kokkos+{backend.lower()}", when=f"+{backend.lower()}", type=("run", "build"))
    # CUDA
    for val in CudaPackage.cuda_arch_values:
        depends_on("kokkos cuda_arch={0}".format(val), when="cuda_arch={0}".format(val))
    # Use +wrapper when not %clang %cce
    depends_on("kokkos+wrapper", when="%gcc+cuda")

    # ROCm
    for val in ROCmPackage.amdgpu_targets:
        depends_on("kokkos amdgpu_target={0}".format(val), when="amdgpu_target={0}".format(val))

    conflicts(
        "+cuda",
        when="+rocm",
        msg="CUDA and ROCm are not compatible in PennyLane-Lightning-Kokkos.",
    )

    # build options
    extends("python")
    variant("cpptests", default=False, description="Build CPP tests")
    variant("native", default=False, description="Build natively for given hardware")
    variant("sanitize", default=False, description="Build with address sanitization")

    # hard dependencies
    depends_on("cmake@3.20:", type="build")
    depends_on("ninja", type="build")
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("python@3.9:", type=("build", "run"), when="@0.32:")
    depends_on("py-setuptools", type="build")
    depends_on("py-pybind11", type="link")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-pennylane@0.28:0.30", type=("build", "run"), when="@:0.30")
    depends_on("py-pennylane@0.30:", type=("build", "run"), when="@0.31")
    # This requirement differs from `pennylane>=0.30` in `setup.py`,
    # but the introduction of `StatePrep` demands `pennylane>=0.32`
    depends_on("py-pennylane@0.32:", type=("build", "run"), when="@0.32")
    depends_on("py-pennylane-lightning~kokkos", type=("build", "run"), when="@:0.31")
    for v in range(33, 38):
        depends_on(f"py-pennylane@0.{v}:", type="run", when=f"@0.{v}")
        depends_on(f"py-pennylane-lightning@0.{v}", type=("build", "run"), when=f"@0.{v}")

    # variant defined dependencies
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    # Test deps
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-mock", type="test")
    depends_on("py-flaky", type="test")

    def url_for_version(self, version):
        extra = "-kokkos" if version <= Version("0.32.0") else ""
        return f"https://github.com/PennyLaneAI/pennylane-lightning{extra}/archive/refs/tags/v{version}.tar.gz"


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    build_directory = "build"

    def setup_build_environment(self, env):
        env.set("PL_BACKEND", "lightning_kokkos")
        cm_args = " ".join([s[2:] for s in self.cmake_args()])
        env.set("CMAKE_ARGS", f"{cm_args}")

    def cmake_args(self):
        """
        Here we specify all variant options that can be dynamically specified at build time
        """
        args_prefix = "PLKOKKOS_" if self.spec.version < Version("0.33") else ""

        args = [
            self.define_from_variant(f"{args_prefix}BUILD_TESTS", "cpptests"),
            self.define_from_variant("PLKOKKOS_ENABLE_NATIVE", "native"),
            self.define_from_variant("PLKOKKOS_ENABLE_SANITIZER", "sanitize"),
        ]
        args.append("-DCMAKE_PREFIX_PATH=" + self.spec["kokkos"].prefix)
        if "+rocm" in self.spec:
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
        args.append(
            "-DPLKOKKOS_ENABLE_WARNINGS=OFF"
        )  # otherwise build might fail due to Kokkos::InitArguments deprecated
        if self.spec.version >= Version("0.33"):
            args.append("-DPL_BACKEND=lightning_kokkos")
        return args

    def build(self, pkg, spec, prefix):
        if self.spec.version < Version("0.32"):
            super().build(pkg, spec, prefix)
            cm_args = ";".join([s[2:] for s in self.cmake_args()])
            args = ["-i", f"--define={cm_args}"]
            python("setup.py", "build_ext", *args)

    def install(self, pkg, spec, prefix):
        pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
        super().install(pkg, spec, prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir(self.stage.source_path):
            pl_device_test = Executable(join_path(self.prefix, "bin", "pl-device-test"))
            pl_device_test("--device", "lightning.kokkos", "--shots", "None", "--skip-ops")
