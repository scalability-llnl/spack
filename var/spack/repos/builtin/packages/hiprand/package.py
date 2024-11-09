# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hiprand(CMakePackage, CudaPackage, ROCmPackage):
    """The hipRAND project provides an interface for generating pseudo-random
    and quasi-random numbers with either cuRAND or rocRAND backends."""

    homepage = "https://github.com/ROCm/hipRAND"
    git = "https://github.com/ROCm/hipRAND.git"
    url = "https://github.com/ROCm/hipRAND/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("cgmb", "srekolam", "renjithravindrankannath")
    libraries = ["libhiprand"]

    license("MIT")

    version("develop", branch="develop")
    version("master", branch="master")
    version("6.2.1", sha256="0d4585b8adbc299f3fdc2c74bb20ffd4285027b861a759c3e62ce564589465da")
    version("6.2.0", sha256="daaf32506eaaf3c3b715ed631387c27992cfe0d938353a88ad6acedc735eb54b")
    version("6.1.2", sha256="f0f129811c144dd711e967305c7af283cefb94bfdbcd2a11296b92a9e966be2c")
    version("6.1.1", sha256="dde1526fb6cde17b18bc9ee6daa719056fc468dfbda5801b9a61260daf2b4498")
    version("6.1.0", sha256="f9d71af23092f8faa888d2c14713ee4d4d350454818ca9331d422c81c2587c1f")
    version("6.0.2", sha256="cb6ff8f58c024b60b3914271921f58f0ab3bdbc9889a53795b40c99c9de0bcd4")
    version("6.0.0", sha256="7e06c98f9da7c0b20b55b2106cf3a48b9ef6577a79549a455667ae97bd15b61d")
    version("5.7.1", sha256="81a9f5f0960dce125ce1ab1c7eb58bb07c8756346f9e46a1cc65aa61d5a114f8")
    version("5.7.0", sha256="4dee76719839503b02ce7d38e1c61bbdb2da18da7f63a7ef7012c84c71aa0a9d")
    version("5.6.1", sha256="a73d5578bc7f8dff0b8960e4bff97bc4fc28f508a19ed6acd1cfd4d3e76b47ee")
    version("5.6.0", sha256="8c214e2f90337a5317a69950026bf337b1e567d43bb9ae64f2a802af2228c313")
    version("5.5.1", sha256="5df9d78eae0991be5ec9f60e8d3530fabc23793d9f9cf274b075d689675db04e")
    version("5.5.0", sha256="7c7dde7b989d5da9c0b0251233245f955b477c090462c7d34e3e0284c5fca761")
    with default_args(deprecated=True):
        version("5.4.3", sha256="7d3d04476880ec90c088dff81f69aac8699eaef972476000e5c4726584ffa98f")
        version("5.4.0", sha256="9456d4b4d5fd5c0b728f4aa4f8c224f829fe6fbf08e397848475293f71029a22")
        version("5.3.3", sha256="f72626b00d61ed2925b3124b7f094ccfaf7750f02bee6bac6b79317e1c5576ef")
        version("5.3.0", sha256="6fd9b3a719bf4c228657cb2a0ff283eb7d777ba31bfffe5a26589d588f89a279")

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
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo"),
        description="CMake build type",
    )
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3.10.2:", type="build")

    depends_on("rocm-cmake@5.2.0:", type="build", when="@5.2.0:")
    depends_on("rocm-cmake@5.1.0:", type="build")

    depends_on("hip +cuda", when="+cuda")

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
        "master",
        "develop",
    ]:
        depends_on("rocrand@" + ver, when="+rocm @" + ver)

    depends_on("rocrand ~hiprand", when="+rocm")
    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(
            "rocrand amdgpu_target={0}".format(tgt), when="+rocm amdgpu_target={0}".format(tgt)
        )

    def setup_build_environment(self, env):
        env.set("CXX", self.spec["hip"].hipcc)
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

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
        args = [self.define("BUILD_BENCHMARK", "OFF"), self.define("BUILD_TEST", self.run_tests)]

        if self.spec.satisfies("+cuda"):
            args.append(self.define("BUILD_WITH_LIB", "CUDA"))
            # FindHIP.cmake is used for +cuda
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))
        else:
            args.append(self.define("BUILD_WITH_LIB", "ROCM"))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append("-DCMAKE_INSTALL_LIBDIR=lib")

        return args
