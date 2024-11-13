# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NlohmannJson(CMakePackage):
    """JSON for Modern C++"""

    homepage = "https://nlohmann.github.io/json/"
    url = "https://github.com/nlohmann/json/archive/v3.1.2.tar.gz"
    maintainers("ax3l")

    license("MIT")

    version("3.11.3", sha256="0d8ef5af7f9794e3263480193c491549b2ba6cc74bb018906202ada498a79406")
    version("3.11.2", sha256="d69f9deb6a75e2580465c6c4c5111b89c4dc2fa94e3a85fcd2ffcd9a143d9273")
    # v3.11.0 & v3.11.1 omitted; released with significant regressions
    version("3.10.5", sha256="5daca6ca216495edf89d167f808d1d03c4a4d929cef7da5e10f135ae1540c7e4")
    version("3.10.4", sha256="1155fd1a83049767360e9a120c43c578145db3204d2b309eba49fbbedd0f4ed3")
    version("3.10.3", sha256="e0d7c1b120cac47fa7f14a41d10a5d390f67d423d8e97b9d6834887285d6873c")
    version("3.10.2", sha256="081ed0f9f89805c2d96335c3acfa993b39a0a5b4b4cef7edb68dd2210a13458c")
    version("3.10.0", sha256="eb8b07806efa5f95b349766ccc7a8ec2348f3b2ee9975ad879259a371aea8084")
    version("3.9.1", sha256="4cf0df69731494668bdd6460ed8cb269b68de9c19ad8c27abc24cd72605b2d5b")
    version("3.9.0", sha256="9943db11eeaa5b23e58a88fbc26c453faccef7b546e55063ad00e7caaaf76d0b")
    version("3.8.0", sha256="7d0edf65f2ac7390af5e5a0b323b31202a6c11d744a74b588dc30f5a8c9865ba")
    version("3.7.2", sha256="914c4af3f14bb98ff084172685fba5d32e8ce4390ec8ba5da45c63daa305df4d")
    version("3.7.0", sha256="d51a3a8d3efbb1139d7608e28782ea9efea7e7933157e8ff8184901efd8ee760")
    version("3.6.1", sha256="80c45b090e40bf3d7a7f2a6e9f36206d3ff710acfa8d8cc1f8c763bb3075e22e")
    version("3.5.0", sha256="e0b1fc6cc6ca05706cce99118a87aca5248bd9db3113e703023d23f044995c1d")
    version("3.4.0", sha256="c377963a95989270c943d522bfefe7b889ef5ed0e1e15d535fd6f6f16ed70732")
    version("3.3.0", sha256="2fd1d207b4669a7843296c41d3b6ac5b23d00dec48dba507ba051d14564aa801")
    version("3.2.0", sha256="2de558ff3b3b32eebfb51cf2ceb835a0fa5170e6b8712b02be9c2c07fcfe52a1")
    version("3.1.2", sha256="e8fffa6cbdb3c15ecdff32eebf958b6c686bc188da8ad5c6489462d16f83ae54")
    version("3.1.1", sha256="9f3549824af3ca7e9707a2503959886362801fb4926b869789d6929098a79e47")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "multiple_headers", default=True, description="Use non-amalgamated version of the library"
    )

    depends_on("cmake@3.8:", type="build")
    depends_on("cmake@3.13:", type="test")

    # requires mature C++11 implementations
    conflicts("%gcc@:4.7")
    # v3.3.0 adds support for gcc 4.8
    # https://github.com/nlohmann/json/releases/tag/v3.3.0
    conflicts("%gcc@:4.8", when="@:3.2.9")
    conflicts("%intel@:16")
    conflicts("%pgi@:14")

    def cmake_args(self):
        return [
            self.define_from_variant("JSON_MultipleHeaders", "multiple_headers"),
            self.define("JSON_BuildTests", self.run_tests),
        ]

    @when("@3.1.1:")
    def check(self):
        # cmake_fetch_content_configure relies on git to fetch a file, fails from tar:
        # https://github.com/nlohmann/json/discussions/2596
        with working_dir(self.build_directory):
            ctest("--output-on-failure", "-LE", "not_reproducible|git_required")
