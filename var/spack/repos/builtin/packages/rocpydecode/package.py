# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocpydecode(CMakePackage):
    """rocPyDecode is a set of Python bindings to rocDecode C++ library which provides
    full HW acceleration for video decoding on AMD GPUs."""

    homepage = "https://github.com/ROCm/rocPyDecode"
    url = "https://github.com/ROCm/rocPyDecode/archive/refs/tags/rocm-6.2.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    version("6.2.1", sha256="34c595cfe40ad74fcec2f52e7cc7be3ad8c8334030b0e98eb36305b6f63edc0d")
    version("6.2.0", sha256="e465254cd3e96bbb59208e90293d7c6b7744b0fbcd928ef278ec568c83e63ff3")

    depends_on("py-pybind11")
    depends_on("ffmpeg@4.4:5")
    depends_on("dlpack")

    for ver in ["6.2.0", "6.2.1"]:
        depends_on(f"rocdecode@{ver}", when=f"@{ver}")

    def patch(self):
        filter_file(
            r"${ROCM_PATH}/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/share/rocdecode/utils",
            "{0}/share/rocdecode/utils".format(self.spec["rocdecode"].prefix),
            "CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = [
            self.define("rocDecode_PATH", self.spec["rocdecode"].prefix),
            self.define("FFMPEG_INCLUDE_DIR", self.spec["ffmpeg"].prefix.include),
            self.define("CMAKE_INSTALL_PREFIX_PYTHON", self.spec.prefix),
            self.define("CMAKE_CXX_FLAGS", "-I{0}".format(self.spec["dlpack"].prefix.include)),
        ]
        return args
