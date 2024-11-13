# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipblas(CMakePackage, CudaPackage, ROCmPackage):
    """hipBLAS is a BLAS marshalling library, with multiple
    supported backends"""

    homepage = "https://github.com/ROCm/hipBLAS"
    git = "https://github.com/ROCm/hipBLAS.git"
    url = "https://github.com/ROCm/hipBLAS/archive/rocm-6.0.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["libhipblas"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.2.1", sha256="b770b6ebd27d5c12ad01827195e996469bfc826e8a2531831df475fc8d7f6b2e")
    version("6.2.0", sha256="33688a4d929b13e1fd800aff7e0833a9f7abf3913754b6b15995595e0d434e94")
    version("6.1.2", sha256="73699892855775a67f48c38beae78169a516078c17f1ed5d67c80abe5d308502")
    version("6.1.1", sha256="087ea82dff13c8162bf93343b174b18f1d58681711bce4fb7c8dc7212020c099")
    version("6.1.0", sha256="5f8193c4ef0508967e608a8adf86d63066a984c5803a4d05dd617021d6298091")
    version("6.0.2", sha256="10c1b6c1deb0f225c0fb6b2bb88398a32cd0d32d3ffce9b5c8df9db2cf88d25c")
    version("6.0.0", sha256="8fbd0c244fe82eded866e06d2399b1d91ab5d43d2ebcb73382c7ce1ae48d9cb3")
    version("5.7.1", sha256="794e9298f48ffbe3bd1c1ab87a5c2c2b953713500155fdec9ef8cbb11f81fc8a")
    version("5.7.0", sha256="8c6cd2ffa4ce6ab03e05feffe074685b5525610870aebe9d78f817b3037f33a4")
    version("5.6.1", sha256="f9da82fbefc68b84081ea0ed0139b91d2a540357fcf505c7f1d57eab01eb327c")
    version("5.6.0", sha256="9453a31324e10ba528f8f4755d2c270d0ed9baa33e980d8f8383204d8e28a563")
    version("5.5.1", sha256="5920c9a9c83cf7e2b42d1f99f5d5091cac7f6c0a040a737e869e57b92d7045a9")
    version("5.5.0", sha256="b080c25cb61531228d26badcdca856c46c640035c058bfc1c9f63de65f418cd5")
    with default_args(deprecated=True):
        version("5.4.3", sha256="5acac147aafc15c249c2f24c19459135ed68b506403aa92e602b67cfc10c38b7")
        version("5.4.0", sha256="341d61adff8d08cbf70aa07bd11a088bcd0687fc6156870a1aee9eff74f3eb4f")
        version("5.3.3", sha256="1ce093fc6bc021ad4fe0b0b93f9501038a7a5a16b0fd4fc485d65cbd220a195e")
        version("5.3.0", sha256="873d55749479873994679840906c4257316dfb09a6200411204ad4a8c2480565")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

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

    depends_on("cmake@3.5:", type="build")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("netlib-lapack@3.7.1:", type="test")
    depends_on("boost@1.64.0:1.76.0 +program_options cxxstd=14", type="test")
    depends_on("py-pyaml", type="test", when="@6.1:")

    patch("remove-hipblas-clients-file-installation.patch", when="@5.5:5.7.1")
    patch("remove-hipblas-clients-file-installation-6.0.patch", when="@6.0:")

    depends_on("rocm-cmake@5.2.0:", type="build", when="@5.2.0:5.7")
    depends_on("rocm-cmake@4.5.0:", type="build")
    for ver in ["6.0.0", "6.0.2", "6.1.0", "6.1.1", "6.1.2", "6.2.0"]:
        depends_on(f"rocm-cmake@{ver}", when=f"+rocm @{ver}")
        depends_on(f"rocm-openmp-extras@{ver}", type="test", when=f"+rocm @{ver}")

    depends_on("hip +cuda", when="+cuda")

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
        "master",
        "develop",
    ]:
        depends_on(f"rocsolver@{ver}", when=f"+rocm @{ver}")
        depends_on(f"rocblas@{ver}", when=f"+rocm @{ver}")
    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(f"rocblas amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")
        depends_on(f"rocsolver amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
            self.define_from_variant("USE_CUDA", "cuda"),
        ]

        # FindHIP.cmake is still used for +cuda
        if self.spec.satisfies("+cuda"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@6.1:") and self.run_tests:
            args.append(self.define("LINK_BLIS", "OFF"))

        return args

    def check(self):
        exe = Executable(
            join_path(self.builder.build_directory, "clients", "staging", "hipblas-test")
        )
        exe("--gtest_filter=-*known_bug*")
