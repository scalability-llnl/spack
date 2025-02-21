# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Quda(CMakePackage, CudaPackage, ROCmPackage):
    """QUDA is a library for performing calculations in lattice QCD on GPUs."""

    homepage = "https://lattice.github.io/quda/"
    url = "https://github.com/lattice/quda/archive/refs/tags/v1.1.0.tar.gz"
    git = "https://github.com/lattice/quda.git"

    tags = ["hep", "lattice"]

    maintainers("chaoos")

    license("MIT OR BSD-3-Clause", checked_by="chaoos")

    version("develop", branch="develop")

    # git describe --tags --match 'v*' 18bf43ed40c75ae276e55bb8ddf2f64aa5510c37
    version(
        "1.1.0-4597-g18bf43ed4", preferred=True, commit="18bf43ed40c75ae276e55bb8ddf2f64aa5510c37"
    )

    version("1.1.0", sha256="b4f635c993275010780ea09d8e593e0713a6ca1af1db6cc86c64518714fcc745")
    version(
        "1.0.0",
        deprecated=True,
        sha256="32b883bd4af45b76a832d8a070ab020306c94ff6590410cbe7c3eab3b630b938",
    )
    version(
        "0.9.0",
        deprecated=True,
        sha256="0a9f2e028fb40e4a09f78af51702d2de4099a9bf10fb8ce350eacb2d8327e481",
    )
    version(
        "0.8.0",
        deprecated=True,
        sha256="58d9a94b7fd38ec1f79bea7a0e9b470f0fa517cbf5fce42d5776e1c65607aeda",
    )

    # build dependencies
    generator("ninja")
    depends_on("cmake@3.18:", type="build")
    depends_on("ninja", type="build")
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+tifr")
    depends_on("fortran", type="build", when="+bqcd")

    variant("mpi", default=False, description="Enable MPI support")
    variant("qmp", default=False, description="Enable QMP")
    variant("qio", default=False, description="Enable QIO")
    variant("openqcd", default=False, description="Enable openQCD interface")
    variant("milc", default=False, description="Enable MILC interface")
    variant("qdp", default=False, description="Enable QDP interface")
    variant("bqcd", default=False, description="Enable BQCD interface")
    variant("cps", default=False, description="Enable CPS interface")
    variant("qdpjit", default=False, description="Enable QDPJIT interface")
    variant("tifr", default=False, description="Enable TIFR interface")
    variant("multigrid", default=False, description="Enable multigrid")
    variant("nvshmem", default=False, description="Enable NVSHMEM", when="+cuda")

    variant("clover", default=False, description="Build clover Dirac operators")
    variant(
        "clover_hasenbusch", default=False, description="Build clover Hasenbusch twist operators"
    )
    variant("domain_wall", default=False, description="Build domain wall Dirac operators")
    variant("laplace", default=False, description="Build laplace operator")
    variant(
        "ndeg_twisted_clover",
        default=False,
        description="Build non-degenerate twisted clover Dirac operators",
    )
    variant(
        "ndeg_twisted_mass",
        default=False,
        description="Build non-degenerate twisted mass Dirac operators",
    )
    variant("staggered", default=False, description="Build staggered Dirac operators")
    variant("twisted_clover", default=False, description="Build twisted clover Dirac operators")
    variant("twisted_mass", default=False, description="Build twisted mass Dirac operators")
    variant("wilson", default=True, description="Build Wilson Dirac operators")

    with when("+multigrid"):
        variant(
            "mg_mrhs_list",
            default=16,
            multi=True,
            description="The list of multi-rhs sizes that get compiled",
        )
        variant(
            "mg_nvec_list",
            default="6,24,32",
            multi=True,
            description="The list of null space vector sizes that get compiled",
        )

    # dependencies
    depends_on("mpi", when="+mpi")
    depends_on("cuda", when="+cuda")
    depends_on("nvshmem", when="+nvshmem")
    depends_on("gdrcopy", when="+nvshmem")
    with when("+rocm"):
        depends_on("hip")
        depends_on("hipblas")
        depends_on("hipfft")
        depends_on("hiprand")
        depends_on("hipcub")

    conflicts("+qmp +mpi", msg="Specifying both QMP and MPI might result in undefined behavior")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="Either CUDA or ROCm support is required")
    conflicts("cuda_arch=none", when="+cuda", msg="Please indicate a cuda_arch value")
    conflicts(
        "+nvshmem", when="~mpi ~qmp", msg="NVSHMEM requires either +mpi or +qmp to be enabled"
    )

    # CMAKE_BUILD_TYPE
    variant(
        "build_type",
        default="STRICT",
        description="The build type to build",
        values=("STRICT", "RELEASE", "DEVEL", "DEBUG", "HOSTDEBUG", "SANITIZE"),
    )

    def cmake_args(self):
        if self.spec.satisfies("+cuda"):
            target = "CUDA"
            cuda_archs = self.spec.variants["cuda_arch"].value
            arch = " ".join(f"sm_{i}" for i in cuda_archs)
        elif self.spec.satisfies("+rocm"):
            target = "HIP"
            arch = self.spec.variants["amdgpu_target"].value

        args = [
            self.define("QUDA_BUILD_ALL_TESTS", False),
            self.define("QUDA_TARGET_TYPE", target),
            self.define("QUDA_GPU_ARCH", arch),
            self.define("QUDA_PRECISION", 14),
            self.define("QUDA_RECONSTRUCT", 7),
            self.define("QUDA_DOWNLOAD_USQCD", False),
            self.define("QUDA_DIRAC_DEFAULT_OFF", True),
            self.define_from_variant("QUDA_DIRAC_CLOVER", "clover"),
            self.define_from_variant("QUDA_DIRAC_CLOVER_HASENBUSCH", "clover_hasenbusch"),
            self.define_from_variant("QUDA_DIRAC_DOMAIN_WALL", "domain_wall"),
            self.define_from_variant("QUDA_DIRAC_LAPLACE", "laplace"),
            self.define_from_variant("QUDA_DIRAC_NDEG_TWISTED_CLOVER", "ndeg_twisted_clover"),
            self.define_from_variant("QUDA_DIRAC_NDEG_TWISTED_MASS", "ndeg_twisted_mass"),
            self.define_from_variant("QUDA_DIRAC_STAGGERED", "staggered"),
            self.define_from_variant("QUDA_DIRAC_TWISTED_CLOVER", "twisted_clover"),
            self.define_from_variant("QUDA_DIRAC_TWISTED_MASS", "twisted_mass"),
            self.define_from_variant("QUDA_DIRAC_WILSON", "wilson"),
            self.define_from_variant("QUDA_MPI", "mpi"),
            self.define_from_variant("QUDA_QMP", "qmp"),
            self.define_from_variant("QUDA_QIO", "qio"),
            self.define_from_variant("QUDA_INTERFACE_OPENQCD", "openqcd"),
            self.define_from_variant("QUDA_INTERFACE_MILC", "milc"),
            self.define_from_variant("QUDA_INTERFACE_QDP", "qdp"),
            self.define_from_variant("QUDA_INTERFACE_BQCD", "bqcd"),
            self.define_from_variant("QUDA_INTERFACE_CPS", "cps"),
            self.define_from_variant("QUDA_INTERFACE_QDPJIT", "qdpjit"),
            self.define_from_variant("QUDA_INTERFACE_TIFR", "tifr"),
            self.define_from_variant("QUDA_MULTIGRID", "multigrid"),
            self.define_from_variant("QUDA_NVSHMEM", "nvshmem"),
        ]
        if self.spec.satisfies("+multigrid"):
            args.append(
                self.define(
                    "QUDA_MULTIGRID_NVEC_LIST", ",".join(self.spec.variants["mg_nvec_list"].value)
                )
            )
            args.append(
                self.define(
                    "QUDA_MULTIGRID_MRHS_LIST", ",".join(self.spec.variants["mg_mrhs_list"].value)
                )
            )

        if self.spec.satisfies("+nvshmem"):
            args.append(self.define("QUDA_NVSHMEM_HOME", self.spec["nvshmem"].prefix))
            args.append(self.define("QUDA_GDRCOPY_HOME", self.spec["gdrcopy"].prefix))

        if self.spec.satisfies("+cuda"):
            args.append(self.define("QUDA_GPU_ARCH_SUFFIX", "real"))  # real or virtual
        elif self.spec.satisfies("+rocm"):
            args.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            # args.append(self.define("ROCM_PATH", self.spec["hip"].prefix))

            # required when building on a machine with no AMD GPU present
            args.append(self.define("AMDGPU_TARGETS", arch))

            # suppress _GLIBCXX17_DEPRECATED warnings when compiling c++17
            args.append(self.define("CMAKE_CXX_FLAGS", "-Wno-deprecated-declarations"))
        return args
