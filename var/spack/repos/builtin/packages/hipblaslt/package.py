# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipblaslt(CMakePackage):
    """hipBLASLt is a library that provides general matrix-matrix operations with a flexible API
    and extends functionalities beyond a traditional BLAS library"""

    homepage = "https://github.com/ROCm/hipBLASLt"
    url = "https://github.com/ROCm/hipBLASLt/archive/refs/tags/rocm-6.1.2.tar.gz"
    git = "https://github.com/ROCm/hipBLASLt.git"

    maintainers("srekolam", "afzpatel", "renjithravindrankannath")

    license("MIT")
    version("6.2.1", sha256="9b062b1d6d945349c31828030c8c1d99fe57d14a1837196ff9aa67bf10ef43f1")
    version("6.2.0", sha256="aec9edc75ae4438aa712192c784e2bed683d2839b502b6aadb18f6012306749b")
    version("6.1.2", sha256="fcfe950f7b87c421565abe090b2de6f463afc1549841002f105ecca7bbbf59e5")
    version("6.1.1", sha256="1e21730ade59b5e32432fa0981383f689a380b1ffc92fe950822722da9521a72")
    version("6.1.0", sha256="90fc2f2c9e11c87e0529e824e4b0561dbc850f8ffa21be6932ae63cbaa27cdf0")
    version("6.0.2", sha256="e281a1a7760fab8c3e0baafe17950cf43c422184e3226e3c14eb06e50c69d421")
    version("6.0.0", sha256="6451b6fdf7f24787628190bbe8f2208c929546b68b692d8355d2f18bea7ca7db")

    depends_on("cxx", type="build")  # generated

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    for ver in ["6.0.0", "6.0.2", "6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"hipblas@{ver}", when=f"@{ver}")
        depends_on(f"rocm-openmp-extras@{ver}", type="test", when=f"@{ver}")

    depends_on("msgpack-c")
    depends_on("py-joblib")
    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")
    depends_on("py-pyyaml", type="test")

    # Sets the proper for clang++ and clang-offload-blunder.
    # Also adds hipblas and msgpack include directories
    patch("001_Set_LLVM_Paths_And_Add_Includes.patch", when="@6.0")
    # Below patch sets the proper path for clang++ and clang-offload-blunder.
    # Also adds hipblas and msgpack include directories for 6.1.0 release.
    patch("0001-Set-LLVM_Path-Add-Hiblas-Include-to-CmakeLists-6.1.Patch", when="@6.1:6.2")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)

    def cmake_args(self):
        args = [
            self.define("Tensile_CODE_OBJECT_VERSION", "default"),
            self.define("MSGPACK_DIR", self.spec["msgpack-c"].prefix),
            self.define_from_variant("ADDRESS_SANITIZER", "asan"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))
        if self.run_tests:
            args.append(
                self.define("ROCM_OPENMP_EXTRAS_DIR", self.spec["rocm-openmp-extras"].prefix)
            )
        return args
