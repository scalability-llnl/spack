# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hipcub(CMakePackage, CudaPackage, ROCmPackage):
    """Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCm/hipCUB"
    git = "https://github.com/ROCm/hipCUB.git"
    url = "https://github.com/ROCm/hipCUB/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    license("BSD-3-Clause")

    maintainers("srekolam", "renjithravindrankannath")
    version("6.2.1", sha256="e0203e72afac4da19cb1d62896fff404ec44517141b420bd38f6e962e52ef6fd")
    version("6.2.0", sha256="8dda8b77740e722fd4cf7223476313fc873bad75d50e6cb86ff284a91d76752d")
    version("6.1.2", sha256="830a0f3231e07fcc6cd6261c4e1af2d7d0ac4862c606ecdc80c2635557ca3d9f")
    version("6.1.1", sha256="967716d67e4270c599a60b770d543ea9148948edb907a0fa4d8be3a1785c2058")
    version("6.1.0", sha256="39ac03053ecf35f1faf212e5b197b03c0104b74b0833f7cce5cf625c273ba71c")
    version("6.0.2", sha256="3f912a23dc34510cf18d9097f6eda37e01d01724975c8149c92a64c92415968c")
    version("6.0.0", sha256="8d9f6e1e3f8433a2ceae1b0efd6727c21383980077e264725d00d5fee165bd30")
    version("5.7.1", sha256="9b23a58408bc4c549d3c754196cb3e2c1a50e177ab0a286101cbea2f7f173945")
    version("5.7.0", sha256="899356867f662d9a6f3870bb4a496f605a3143c6ad4d1fa9e9faead68fa8d13b")
    version("5.6.1", sha256="4b9479daa40424c9ddbc14ce967aa170680f8ca1ed01a514e6e30ccfa22552ce")
    version("5.6.0", sha256="5e74ddbf833f39836bf9ec6c6750348c7386a85ca67aaf9bb54d16c9e1959031")
    version("5.5.1", sha256="ad83f3f1ed85ead9e3012906957c125a896168be913f6fb6af298228fc571480")
    version("5.5.0", sha256="3eec838119326a67eb4cc006c706e328f3a51a01e98bbfb518df8fe4a4707e13")
    with default_args(deprecated=True):
        version("5.4.3", sha256="cf528d9acb4f9b9c3aad439ae76bfc3d02be6e7a74d96099544e5d54e1a23675")
        version("5.4.0", sha256="78db2c2ea466a4c5d84beedc000ae934f6d0ff1793eae90bb8d02b2dbff8932c")
        version("5.3.3", sha256="b4fc3c05892729873dc098f111c31f83af7d33da572bdb7d87de100d4c238e6d")
        version("5.3.0", sha256="4016cfc240b3cc1a97b549ecc4a5b76369610d46247661834630846391e5fad2")

    depends_on("cxx", type="build")  # generated

    # default to an 'auto' variant until amdgpu_targets can be given a better default than 'none'
    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.DisjointSetsOfValues(("auto",), ("none",), amdgpu_targets)
        .with_default("auto")
        .with_error(
            "the values 'auto' and 'none' are mutually exclusive with any of the other values"
        )
        .with_non_feature_values("auto", "none"),
        sticky=True,
    )
    variant("rocm", default=True, description="Enable ROCm support")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")

    depends_on("cmake@3.10.2:", type="build")

    depends_on("googletest@1.10.0:", type="test")

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
    ]:
        depends_on(f"rocprim@{ver}", when=f"+rocm @{ver}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"hip +cuda@{ver}", when=f"+cuda @{ver}")

    # fix hardcoded search in /opt/rocm and broken config mode search
    patch("find-hip-cuda-rocm-5.3.patch", when="@5.3: +cuda")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+rocm"):
            env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

    def cmake_args(self):
        args = [self.define("BUILD_TEST", self.run_tests)]

        if self.spec.satisfies("+rocm ^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        # FindHIP.cmake is still used for +cuda
        if self.spec.satisfies("+cuda"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        return args
