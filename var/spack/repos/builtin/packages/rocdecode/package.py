# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocdecode(CMakePackage):
    """rocDecode is a high performance video decode SDK for AMD hardware"""

    homepage = "https://github.com/ROCm/rocDecode"
    git = "https://github.com/ROCm/rocDecode.git"
    url = "https://github.com/ROCm/rocDecode/archive/refs/tags/rocm-6.2.0.tar.gz"

    tags = ["rocm"]

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")
    version("6.2.1", sha256="d4a636415d61fef94f97197cb9ebbff59e3a18dc4850612ee142e3e14a35e6d4")
    version("6.2.0", sha256="fe0d7c19a4e65b93405566511880b94f25ef68c830d0088f9458da9baea1d4f9")
    version("6.1.2", sha256="67a13aeaa495e06683124de5908e61cf2be3beff79b13d858897344aa809775e")
    version("6.1.1", sha256="5914c91e433ec7e8511b8a9017d165a0589c1aff9f5527b413d0b3a32a3cc318")
    version("6.1.0", sha256="8316dbde87f1fea782af6216c8d013e866542329a673fb24a668335c6169ef8f")

    amdgpu_targets = ROCmPackage.amdgpu_targets

    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=auto_or_any_combination_of(*amdgpu_targets),
        sticky=True,
    )

    for ver in ["6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on(f"hip@{ver}", when=f"@{ver}")

    def patch(self):
        filter_file(
            r"${ROCM_PATH}/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = []
        if "auto" not in self.spec.variants["amdgpu_target"]:
            args.append(self.define_from_variant("AMDGPU_TARGETS", "amdgpu_target"))
        return args
