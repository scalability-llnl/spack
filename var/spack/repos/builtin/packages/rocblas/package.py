# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Rocblas(CMakePackage):
    """Radeon Open Compute BLAS library"""

    homepage = "https://github.com/ROCm/rocBLAS/"
    git = "https://github.com/ROCm/rocBLAS.git"
    url = "https://github.com/ROCm/rocBLAS/archive/rocm-6.1.1.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath", "haampie")
    libraries = ["librocblas"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.2.1", sha256="cf3bd7b47694f95f387803191615e2ff5c1106175473be7a5b2e8eb6fb99179f")
    version("6.2.0", sha256="184e9b39dcbed57c25f351b047d44c613f8a2bbab3314a20c335f024a12ad4e5")
    version("6.1.2", sha256="1e83918bd7b28ec9ee292c6fb7eb0fc5f4db2d5d831a9a3db541f14a90c20a1a")
    version("6.1.1", sha256="c920742fb8f45512c360cdb40e37d0ac767f042e52f1981264853dab5ec2c876")
    version("6.1.0", sha256="af00357909da60d82618038aa9a3cc1f9d4ce1bdfb54db20ec746b592d478edf")
    version("6.0.2", sha256="d1bf31063a2d349797b88c994c91d05f94e681bafb5550ad9b53529703d89dbb")
    version("6.0.0", sha256="befa4a75f1de0ea37f2358d4c2de5406d7bce671ca9936e2294b64d3b3bafb60")
    version("5.7.1", sha256="2984a5ed0ea5a05d40996ee3fddecb24399cbe8ea3e4921fc254e54d8f52fe4f")
    version("5.7.0", sha256="024edd98de9687ee5394badc4dd4c543eef4eb3f71c96ff64100705d851e1744")
    version("5.6.1", sha256="73896ebd445162a69af97f9fd462684609b4e0cf617eab450cd4558b4a23941e")
    version("5.6.0", sha256="6a70b27eede02c45f46095a6ce8421af9a774a565e39f5e1074783ecf00c1ea7")
    version("5.5.1", sha256="7916a8d238d51cc239949d799f0b61c9d5cd63c6ccaed0e16749489b89ca8ff3")
    version("5.5.0", sha256="b5260517f199e806ae18f2c4495f163884e0d7a0a7c67af0770f7428ea50f898")
    with default_args(deprecated=True):
        version("5.4.3", sha256="d82cd334b7a9b40d16ec4f4bb1fb5662382dcbfc86ee5e262413ed63d9e6a701")
        version("5.4.0", sha256="261e05375024a01e68697c5d175210a07f0f5fc63a756234d996ddedffde78a2")
        version("5.3.3", sha256="62a3b5f415bd8e0dcd0d68233d379f1a928ec0349977c32b4eea72ae5004e805")
        version("5.3.0", sha256="8ea7269604cba949a6ea84b78dc92a44fa890427db88334da6358813f6512e34")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("tensile", default=True, description="Use Tensile as a backend")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    # https://reviews.llvm.org/D124866
    # https://github.com/ROCm/HIP/issues/2678
    # https://github.com/ROCm/hipamd/blob/rocm-5.2.x/include/hip/amd_detail/host_defines.h#L50
    conflicts("%gcc@12", when="@5.2")

    depends_on("cmake@3.16.8:", type="build")

    depends_on("googletest@1.10.0:", type="test")
    depends_on("amdblis", type="test")

    for ver in [
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
        depends_on(f"rocm-openmp-extras@{ver}", type="test", when=f"@{ver}")

    for ver in ["6.2.0", "6.2.1"]:
        depends_on(f"rocm-smi-lib@{ver}", type="test", when=f"@{ver}")

    depends_on("rocm-cmake@master", type="build", when="@master:")

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
        depends_on(f"hip@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", type="build", when=f"@{ver}")
        depends_on(f"rocminfo@{ver}", type="build", when=f"@{ver}")
        depends_on(f"rocm-cmake@{ver}", type="build", when=f"@{ver}")

    depends_on("python@3.6:", type="build")

    with when("+tensile"):
        depends_on("msgpack-c@3:")

        depends_on("py-virtualenv", type="build")
        depends_on("perl-file-which", type="build")
        depends_on("py-pyyaml", type="build")
        depends_on("py-wheel", type="build")
        depends_on("py-msgpack", type="build")
        depends_on("py-pip", type="build")
        depends_on("py-joblib", type="build", when="@5.6:")
        depends_on("procps", type="build", when="@5.6:")

    for t_version, t_commit in [
        ("@5.3.0", "b33ca97af456cda14f7b1ec9bcc8aeab3ed6dd08"),
        ("@5.3.3", "006a5d653ce0d82fecb05d5e215d053749b57c04"),
        ("@5.4.0", "5aec08937473b27865fa969bb38a83bcf9463c2b"),
        ("@5.4.3", "5aec08937473b27865fa969bb38a83bcf9463c2b"),
        ("@5.5.0", "38d444a9f2b6cddfeaeedcb39a5688150fa27093"),
        ("@5.5.1", "38d444a9f2b6cddfeaeedcb39a5688150fa27093"),
        ("@5.6.0", "7d0a9d040c3bbae893df7ecef6a19d9cd1c304aa"),
        ("@5.6.1", "7d0a9d040c3bbae893df7ecef6a19d9cd1c304aa"),
        ("@5.7.0", "97e0cfc2c8cb87a1e38901d99c39090dc4181652"),
        ("@5.7.1", "97e0cfc2c8cb87a1e38901d99c39090dc4181652"),
        ("@6.0.0", "17df881bde80fc20f997dfb290f4bb4b0e05a7e9"),
        ("@6.0.2", "17df881bde80fc20f997dfb290f4bb4b0e05a7e9"),
        ("@6.1.0", "2b55ccf58712f67b3df0ca53b0445f094fcb96b2"),
        ("@6.1.1", "2b55ccf58712f67b3df0ca53b0445f094fcb96b2"),
        ("@6.1.2", "2b55ccf58712f67b3df0ca53b0445f094fcb96b2"),
        ("@6.2.0", "dbc2062dced66e4cbee8e0591d76e0a1588a4c70"),
        ("@6.2.1", "dbc2062dced66e4cbee8e0591d76e0a1588a4c70"),
    ]:
        resource(
            name="Tensile",
            git="https://github.com/ROCm/Tensile.git",
            commit=t_commit,
            when=f"{t_version} +tensile",
        )

    for ver in ["master", "develop"]:
        resource(
            name="Tensile",
            git="https://github.com/ROCm/Tensile.git",
            branch=ver,
            when=f"@{ver} +tensile",
        )

    # Finding Python package and set command python as python3
    patch("0004-Find-python.patch", when="@5.2.0:5.4")
    patch("0006-Guard-use-of-OpenMP-to-make-it-optional-5.4.patch", when="@5.4")
    patch("0007-add-rocm-openmp-extras-include-dir.patch", when="@5.6:5.7")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

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

    def cmake_args(self):
        args = [
            self.define("BUILD_CLIENTS_TESTS", self.run_tests and "@4.2.0:" in self.spec),
            self.define("BUILD_CLIENTS_BENCHMARKS", "OFF"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("RUN_HEADER_TESTING", "OFF"),
            self.define_from_variant("BUILD_WITH_TENSILE", "tensile"),
        ]
        if self.run_tests:
            args.append(self.define("LINK_BLIS", "ON"))
            if self.spec.satisfies("@5.6.0:"):
                args.append(
                    self.define("ROCM_OPENMP_EXTRAS_DIR", self.spec["rocm-openmp-extras"].prefix)
                )
                args.append(
                    self.define("BLIS_INCLUDE_DIR", self.spec["amdblis"].prefix + "/include/blis/")
                )
                args.append(
                    self.define("BLAS_LIBRARY", self.spec["amdblis"].prefix + "/lib/libblis.a")
                )

        if "+tensile" in self.spec:
            tensile_path = join_path(self.stage.source_path, "Tensile")
            args += [
                self.define("Tensile_TEST_LOCAL_PATH", tensile_path),
                self.define("Tensile_COMPILER", "hipcc"),
                self.define("Tensile_LOGIC", "asm_full"),
                self.define("BUILD_WITH_TENSILE_HOST", "@3.7.0:" in self.spec),
                self.define("Tensile_LIBRARY_FORMAT", "msgpack"),
            ]
            # Restrict the number of jobs Tensile can spawn.
            # If we don't specify otherwise, Tensile creates a job per available core,
            # and that consumes a lot of system memory.
            # https://github.com/ROCm/Tensile/blob/93e10678a0ced7843d9332b80bc17ebf9a166e8e/Tensile/Parallel.py#L38
            args.append(self.define("Tensile_CPU_THREADS", min(16, make_jobs)))

        # See https://github.com/ROCm/rocBLAS/commit/c1895ba4bb3f4f5947f3818ebd155cf71a27b634
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        # See https://github.com/ROCm/rocBLAS/issues/1196
        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))
        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        if self.spec.satisfies("@:5.4"):
            args.append(self.define("Tensile_CODE_OBJECT_VERSION", "V3"))
        else:
            args.append(self.define("Tensile_CODE_OBJECT_VERSION", "default"))

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = Executable(join_path(self.build_directory, "clients", "staging", "rocblas-test"))
        exe("--gtest_filter=*quick*-*known_bug*")
