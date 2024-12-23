# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocal(CMakePackage):
    """The AMD rocAL is designed to efficiently decode and process images and videos from a variety
    of storage formats and modify them through a processing graph programmable by the user."""

    homepage = "https://github.com/ROCm/rocAL"
    url = "https://github.com/ROCm/rocAL/archive/refs/tags/rocm-6.2.0.tar.gz"

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.3.0", sha256="162a0c15e6e7e09c0e13a9d01a493ba3199b77919addf396cd5d273ebf44d759")
    version("6.2.4", sha256="630813669e75a8ee179b89f489101931a26f7a7ee486fcbe1b0e3cb1803c582c")
    version("6.2.1", sha256="77d3e63e02afaee6f1ee1d877d88b48c6ea66a0afca96a1313d0f1c4f8e86b2a")
    version("6.2.0", sha256="c7c265375a40d4478a628258378726c252caac424f974456d488fce43890e157")

    depends_on("libjpeg-turbo@2.0.6+partial_decoder", when="@6.2.0")
    depends_on("libjpeg-turbo@3.0.2:", when="@6.2.1:")
    depends_on("rapidjson")
    depends_on("ffmpeg@4.4:")

    for ver in ["6.2.0", "6.2.1", "6.2.4", "6.3.0"]:
        depends_on(f"mivisionx@{ver}", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        depends_on(f"rpp@{ver}", when=f"@{ver}")

    def patch(self):
        filter_file(
            r"${ROCM_PATH}/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "rocAL/rocAL_hip/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/lib/llvm/bin/clang++",
            "{0}/bin/clang++".format(self.spec["llvm-amdgpu"].prefix),
            "rocAL/rocAL_hip/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/include/rocal",
            "{0}/include/rocal".format(self.spec.prefix),
            "tests/cpp_api/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/${CMAKE_INSTALL_INCLUDEDIR}/rocal",
            "{0}/include/rocal".format(self.spec.prefix),
            "tests/cpp_api/audio_tests/CMakeLists.txt",
            "tests/cpp_api/image_augmentation/CMakeLists.txt",
            "tests/cpp_api/basic_test/CMakeLists.txt",
            "tests/cpp_api/performance_tests/CMakeLists.txt",
            "tests/cpp_api/dataloader/CMakeLists.txt",
            "tests/cpp_api/performance_tests_with_depth/CMakeLists.txt",
            "tests/cpp_api/dataloader_multithread/CMakeLists.txt",
            "tests/cpp_api/unit_tests/CMakeLists.txt",
            "tests/cpp_api/dataloader_tf/CMakeLists.txt",
            "tests/cpp_api/video_tests/CMakeLists.txt",
            "tests/cpp_api/external_source/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/lib",
            "{0}/lib".format(self.spec.prefix),
            "tests/cpp_api/audio_tests/CMakeLists.txt",
            "tests/cpp_api/image_augmentation/CMakeLists.txt",
            "tests/cpp_api/basic_test/CMakeLists.txt",
            "tests/cpp_api/performance_tests/CMakeLists.txt",
            "tests/cpp_api/dataloader/CMakeLists.txt",
            "tests/cpp_api/performance_tests_with_depth/CMakeLists.txt",
            "tests/cpp_api/dataloader_multithread/CMakeLists.txt",
            "tests/cpp_api/unit_tests/CMakeLists.txt",
            "tests/cpp_api/dataloader_tf/CMakeLists.txt",
            "tests/cpp_api/video_tests/CMakeLists.txt",
            "tests/cpp_api/external_source/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/lib",
            "{0}/lib".format(self.spec.prefix),
            "tests/cpp_api/CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"${ROCM_PATH}/share/rocal",
            "{0}/share/rocal".format(self.spec.prefix),
            "tests/cpp_api/CMakeLists.txt",
            string=True,
        )

    def cmake_args(self):
        args = [
            self.define("AMDRPP_PATH", self.spec["rpp"].prefix),
            self.define("TURBO_JPEG_PATH", self.spec["libjpeg-turbo"].prefix),
            self.define("MIVisionX_PATH", self.spec["mivisionx"].prefix),
            self.define("CMAKE_INSTALL_PREFIX_PYTHON", self.spec.prefix),
        ]
        return args

    def check(self):
        print("test will run after install")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        with working_dir(self.build_directory, create=True):
            make("test")
