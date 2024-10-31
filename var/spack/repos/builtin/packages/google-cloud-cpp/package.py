# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GoogleCloudCpp(CMakePackage):
    """C++ Client Libraries for Google Cloud Platform."""

    homepage = "https://cloud.google.com/cpp"
    url = "https://github.com/googleapis/google-cloud-cpp/archive/refs/tags/v2.28.0.tar.gz"

    maintainers("dbolduc")

    license("Apache-2.0", checked_by="dbolduc")

    sanity_check_is_dir = ["lib", "include"]

    version("2.28.0", sha256="1d51910cb4419f6100d8b9df6bccd33477d09f50e378f12b06dae0f137ed7bc6")

    depends_on("abseil-cpp")
    depends_on("curl")
    depends_on("google-crc32c")
    depends_on("grpc")
    depends_on("nlohmann-json")
    depends_on("protobuf")

    variant("shared", default=False, description="Build shared instead of static libraries")
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            "-DBUILD_TESTING:Bool=OFF",
            "-DGOOGLE_CLOUD_CPP_WITH_MOCKS:Bool=OFF",
            "-DGOOGLE_CLOUD_CPP_ENABLE_EXAMPLES:Bool=OFF",
            "-DGOOGLE_CLOUD_CPP_ENABLE:String=__ga_libraries__",
        ]
        return args
