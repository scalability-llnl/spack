# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pthreadpool(CMakePackage):
    """pthreadpool is a portable and efficient thread pool implementation."""

    homepage = "https://github.com/Maratyszcza/pthreadpool"
    git = "https://github.com/Maratyszcza/pthreadpool.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("2023-08-29", commit="4fe0e1e183925bf8cfa6aae24237e724a96479b8")  # py-torch@2.2:
    version("2021-04-13", commit="a134dd5d4cee80cce15db81a72e7f929d71dd413")  # py-torch@1.9:2.1
    version("2020-10-05", commit="fa75e65a58a5c70c09c30d17a1fe1c1dff1093ae")  # py-torch@1.8
    version("2020-06-15", commit="029c88620802e1361ccf41d1970bd5b07fd6b7bb")  # py-torch@1.6:1.7
    version("2019-10-29", commit="d465747660ecf9ebbaddf8c3db37e4a13d0c9103")  # py-torch@1.5
    version("2018-10-08", commit="13da0b4c21d17f94150713366420baaf1b5a46f4")  # py-torch@1.0:1.4
    version("2018-02-25", commit="2b06b31f6a315162348e1f3c24325eedaf6cc559")  # py-torch@:0.4

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")

    resource(
        name="fxdiv",
        git="https://github.com/Maratyszcza/FXdiv.git",
        branch="master",
        destination="deps",
        placement="fxdiv",
    )
    resource(
        name="googletest",
        url="https://github.com/google/googletest/archive/release-1.12.0.zip",
        sha256="ce7366fe57eb49928311189cb0e40e0a8bf3d3682fca89af30d884c25e983786",
        destination="deps",
        placement="googletest",
    )
    resource(
        name="googlebenchark",
        url="https://github.com/google/benchmark/archive/v1.5.3.zip",
        sha256="bdefa4b03c32d1a27bd50e37ca466d8127c1688d834800c38f3c587a396188ee",
        destination="deps",
        placement="googlebenchmark",
    )

    def cmake_args(self):
        return [
            self.define("FXDIV_SOURCE_DIR", join_path(self.stage.source_path, "deps", "fxdiv")),
            self.define(
                "GOOGLETEST_SOURCE_DIR", join_path(self.stage.source_path, "deps", "googletest")
            ),
            self.define(
                "GOOGLEBENCHMARK_SOURCE_DIR",
                join_path(self.stage.source_path, "deps", "googlebenchmark"),
            ),
            # https://github.com/pytorch/pytorch/blob/main/cmake/Dependencies.cmake
            self.define("PTHREADPOOL_BUILD_TESTS", False),
            self.define("PTHREADPOOL_BUILD_BENCHMARKS", False),
            self.define("PTHREADPOOL_LIBRARY_TYPE", "static"),
            self.define("PTHREADPOOL_ALLOW_DEPRECATED_API", True),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]
