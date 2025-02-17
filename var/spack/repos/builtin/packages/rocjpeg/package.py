# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rocjpeg(CMakePackage):
    """rocJPEG is a high-performance jpeg decode SDK for decoding jpeg images
    using a hardware-accelerated jpeg decoder on AMD's GPUs."""

    homepage = "https://github.com/ROCm/rocJPEG"
    git = "https://github.com/ROCm/rocJPEG.git"
    url = "https://github.com/ROCm/rocJPEG/archive/refs/tags/rocm-6.3.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.3.2", sha256="4e1ec9604152e818afa85360f1e0ef9e98bfb8a97ca0989980063e2ece015c16")
    version("6.3.1", sha256="f4913cbc63e11b9b418d33b0f9ba0fec0aa00b23285090acfd435e1ba1c21e42")
    version("6.3.0", sha256="2623b8f8bb61cb418d00c695e8ff0bc5979e1bb2d61d6c327a27d676c89e89cb")

    depends_on("cxx", type="build")

    for ver in ["6.3.0", "6.3.1", "6.3.2"]:
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"hip@{ver}", when=f"@{ver}")

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
