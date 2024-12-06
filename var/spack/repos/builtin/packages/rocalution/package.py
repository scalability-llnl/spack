# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import re

from spack.package import *


class Rocalution(CMakePackage):
    """rocALUTION is a sparse linear algebra library with focus on
    exploring fine-grained parallelism on top of AMD's Radeon Open
    eCosystem Platform ROCm runtime and toolchains, targeting modern
    CPU and GPU platforms. Based on C++ and HIP, it provides a portable,
     generic and flexible design that allows seamless integration with
    other scientific software packages."""

    homepage = "https://github.com/ROCm/rocALUTION"
    git = "https://github.com/ROCm/rocALUTION.git"
    url = "https://github.com/ROCm/rocALUTION/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["librocalution_hip"]

    license("MIT")
    version("6.2.1", sha256="94f15add5316c81529ce84ae8bf2701e9a4df57d08eda04a2f70147d31b12632")
    version("6.2.0", sha256="fd9ad0aae5524d3995343d4d7c1948e7b21f0bdf5b1203d1de58548a814a9c39")
    version("6.1.2", sha256="5f9fb302ab1951a1caf54ed31b41d6f41a353dd4b5ee32bc3de2e9f9244dd4ef")
    version("6.1.1", sha256="1f80b33813291c2e81e5b1efc325d3f5bb6592c8670c016930d01e73e74ab46b")
    version("6.1.0", sha256="699a9b73844fcd4e30d0607b4042dc779f9bcdc27ad732e7a038968ff555af2b")
    version("6.0.2", sha256="453f889677728b510286d4c72952b343cac63c45e2cb8b801d8388a2ec599d2a")
    version("6.0.0", sha256="cabf37691b8db00c82bda49c7dcfaefd9b9067b7d097afa43b7a5f86c45bff99")
    version("5.7.1", sha256="b95afa1285759843c5fea1ad6e1c1edf283922e0d448db03a3e1f42b6942bc24")
    version("5.7.0", sha256="48232a0d1250debce89e39a233bd0b5d52324a2454c078b99c9d44965cbbc0e9")
    version("5.6.1", sha256="7197b3617a0c91e90adaa32003c04d247a5f585d216e77493d20984ba215addb")
    version("5.6.0", sha256="7397a2039e9615c0cf6776c33c4083c00b185b5d5c4149c89fea25a8976a3097")
    version("5.5.1", sha256="4612e30a0290b1732c8862eea655122abc2d22ce4345b8498fe4127697e880b4")
    version("5.5.0", sha256="626e966b67b83a1ef79f9bf27aba998c49cf65c4208092516aa1e32a6cbd8c36")
    with default_args(deprecated=True):
        version("5.4.3", sha256="39d00951a9b3cbdc4205a7e3ce75c026d9428c71c784815288c445f84a7f8a0e")
        version("5.4.0", sha256="dccf004434e0fee6d0c7bedd46827f5a2af0392bc4807a08403b130e461f55eb")
        version("5.3.3", sha256="3af022250bc25bebdee12bfb8fdbab4b60513b537b9fe15dfa82ded8850c5066")
        version("5.3.0", sha256="f623449789a5c9c9137ae51d4dbbee5c6940d8813826629cb4b7e84f07fab494")

    depends_on("cxx", type="build")  # generated

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("cmake@3.5:", type="build")

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
        depends_on(f"rocprim@{ver}", when=f"@{ver}")
        for tgt in itertools.chain(["auto"], amdgpu_targets):
            rocblas_tgt = tgt if tgt != "gfx900:xnack-" else "gfx900"
            depends_on(
                f"rocblas@{ver} amdgpu_target={rocblas_tgt}", when=f"@{ver} amdgpu_target={tgt}"
            )
            depends_on(f"rocsparse@{ver} amdgpu_target={tgt}", when=f"@{ver} amdgpu_target={tgt}")
            depends_on(f"rocrand@{ver} amdgpu_target={tgt}", when=f"@{ver} amdgpu_target={tgt}")
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")

    depends_on("googletest@1.10.0:", type="test")
    # Fix build for most Radeon 5000 and Radeon 6000 series GPUs.
    patch("0004-fix-navi-1x.patch", when="@5.2.0:5.3")

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            env.set("CC", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang")
            env.set("CXX", f"{self.spec['llvm-amdgpu'].prefix}/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    def patch(self):
        with working_dir("src/base/hip"):
            filter_file(
                "^#include <rocrand/rocrand.hpp>",
                "#include <rocrand.hpp>",
                "hip_rand_normal.hpp",
                "hip_rand_uniform.hpp",
            )

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    def cmake_args(self):
        args = [
            self.define("SUPPORT_HIP", "ON"),
            self.define("SUPPORT_MPI", "OFF"),
            self.define("BUILD_CLIENTS_SAMPLES", "OFF"),
            self.define("BUILD_CLIENTS_TESTS", self.run_tests),
        ]
        if self.spec.satisfies("@5.2:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))

        if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
            args.append(self.define("__skip_rocmclang", "ON"))

        if self.spec.satisfies("@5.2:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = Executable(join_path(self.build_directory, "clients", "staging", "rocalution-test"))
        exe()
