# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diy(CMakePackage):
    """Data-parallel out-of-core library"""

    homepage = "https://github.com/diatomic/diy"
    maintainers("vicentebolea")

    url = "https://github.com/diatomic/diy/archive/3.6.0.tar.gz"
    git = "https://github.com/diatomic/diy.git"

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("3.6.0", sha256="d12eb7dabe3a8a66cd406d34aabdb43c1ec178b7ed40cf1dff10016643bbf149")
    version("3.5.0", sha256="b3b5490441d521b6e9b33471c782948194bf95c7c3df3eb97bc5cf4530b91576")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    # https://gitlab.kitware.com/diatomic/diy/-/merge_requests/82
    patch(
        "https://gitlab.kitware.com/diatomic/diy/-/commit/1d85dd5205b9f0035840e1840a49ea7028618d16.diff",
        sha256="047bed205c905064923d7ecf1d03e38c07f3ae0baa0f4afe1b234f68315472d3",
        when="@3.6:",
    )

    def cmake_args(self):
        args = [
            "-Dbuild_examples=off",
            "-Dbuild_tests=off",
            "-Dinstall_examples=on",
            "-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx,
        ]
        return args

    def test_smoke_test(self):
        """Build and run ctests"""
        spec = self.spec

        if spec.satisfies("@:3.5"):
            raise SkipTest("Smoke test requires DIY>=3.6")

        with working_dir("smoke_test_build", create=True):
            cmake = Executable(spec["cmake"].prefix.bin.cmake)
            ctest = Executable(spec["cmake"].prefix.bin.ctest)

            cmake(
                spec["diy"].prefix.share.DIY.examples.smoke_test,
                f"-DMPI_HOME={spec['mpi'].prefix}",
                f"-DCMAKE_PREFIX_PATH={spec['diy'].prefix}",
            )
            cmake("--build", ".")
            ctest("--verbose")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        self.test_smoke_test()
