# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocjpeg(CMakePackage):
    """rocJPEG is a high-performance jpeg decode SDK for decoding jpeg images
    using a hardware-accelerated jpeg decoder on AMD's GPUs."""

    homepage = "https://rocm.docs.amd.com/projects/rocJPEG/en/latest/"
    url = "https://github.com/ROCm/rocJPEG/archive/refs/tags/rocm-6.3.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.3.0", sha256="2623b8f8bb61cb418d00c695e8ff0bc5979e1bb2d61d6c327a27d676c89e89cb")

    depends_on("cxx", type="build")

    depends_on("hip@6.3.0", when="@6.3.0")
    depends_on("libva", type="build", when="@6.2:")

    def patch(self):
        filter_file(
            r"${ROCM_PATH}/lib/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = [self.define("LIBVA_INCLUDE_DIR", self.spec["libva"].prefix.include)]
        return args
