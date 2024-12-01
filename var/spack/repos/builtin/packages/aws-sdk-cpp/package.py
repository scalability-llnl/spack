# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwsSdkCpp(CMakePackage):
    """AWS SDK for C++.

    The AWS SDK for C++ provides a modern C++ (version C++ 11 or later) interface for
    Amazon Web Services (AWS). It is meant to be performant and fully functioning with
    low- and high-level SDKs, while minimizing dependencies and providing platform
    portability (Windows, OSX, Linux, and mobile).
    """

    homepage = "https://github.com/aws/aws-sdk-cpp"
    git = "https://github.com/aws/aws-sdk-cpp.git"

    license("Apache-2.0")

    version(
        "1.11.144",
        tag="1.11.144",
        commit="498339d47146f8e3ee9ae0fad3fcda5acbaea1e6",
        submodules=True,
    )
    version(
        "1.10.57",
        tag="1.10.57",
        commit="777e0dd4b90eda8bf65bc4b5fce2f90febdbd2b8",
        submodules=True,
    )
    version(
        "1.10.32",
        tag="1.10.32",
        commit="40594bc05a3f68fe14f2f1a54c5c3e6752b1e290",
        submodules=True,
    )
    version(
        "1.9.379",
        tag="1.9.379",
        commit="94d02db44730b0a5cef98ce33deedf43f5333700",
        submodules=True,
    )
    version(
        "1.9.247",
        tag="1.9.247",
        commit="4bf33aa0172704eb5fc1da8086686670711bd801",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("zlib-api")
    depends_on("curl")

    # https://github.com/aws/aws-sdk-cpp/issues/1816
    patch(
        "https://github.com/aws/aws-sdk-cpp/pull/1937.patch?full_index=1",
        sha256="ba86e0556322604fb4b70e2dd4f4fb874701868b07353fc1d5c329d90777bf45",
        when="@1.9.247",
    )

    def cmake_args(self):
        return [
            self.define("BUILD_ONLY", ("s3", "transfer")),
            self.define("ENABLE_TESTING", False),
            self.define("AUTORUN_UNIT_TESTS", False),
        ]
