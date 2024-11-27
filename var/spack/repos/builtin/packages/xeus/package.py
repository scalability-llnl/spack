# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xeus(CMakePackage):
    """QuantStack C++ implementation of Jupyter kernel protocol"""

    homepage = "https://xeus.readthedocs.io/en/latest/"
    url = "https://github.com/QuantStack/xeus/archive/0.14.1.tar.gz"
    git = "https://github.com/QuantStack/xeus.git"

    maintainers("tomstitt")

    license("BSD-3-Clause")

    version("develop", branch="master")
    version("1.0.4", sha256="7324ff013eb97d579fd3b6f9770a13f8863d6046c8bbcdbe2fc7d2ac02f0161f")
    version("0.15.0", sha256="bc99235b24d5757dc129f3ed531501fb0d0667913927ed39ee24281952649183")
    version("0.14.1", sha256="a6815845d4522ec279f142d3b4e92ef52cd80847b512146a65f256a77e058cfe")

    depends_on("cxx", type="build")  # generated

    variant("examples", default=False, description="Build examples")
    variant("shared", default=True, description="Build shared libraries")

    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.6")
    conflicts("%intel@:17")

    depends_on("libzmq@4.2.5:-libsodium")
    depends_on("cppzmq@4.7.1:", when="@1.0.4:")
    depends_on("cppzmq@4.3.0:", when="@:0.15.0")

    depends_on("cryptopp@7.0.0:", when="@:0.15.0")

    depends_on("openssl@1.0.1:", when="@1.0.4:")

    depends_on("xtl@0.4.0:", when="@:0.15.0")
    depends_on("xtl@0.7.0:0.7", when="@1.0.4:")

    depends_on("nlohmann-json@3.4.0:", when="@1.0.4:")
    depends_on("nlohmann-json@3.2.0", when="@0.15.0")
    depends_on("nlohmann-json@3.1.1", when="@0.14.1")

    depends_on("uuid", when="platform=linux")

    # finds cryptopp not built with cmake, removes c++17 attribute
    # in check_cxx_source_compiles
    patch("cmake_find_cryptopp_and_check_cxx_compatibility.patch", when="@:0.15.0")

    def cmake_args(self):
        args = []

        if "@:0.15.0" in self.spec:
            args.append(self.define_from_variant("BUILD_EXAMPLES", "examples"))

        elif "@1.0.4:" in self.spec:
            args.extend(
                [
                    self.define_from_variant("XEUS_BUILD_SHARED_LIBS", "shared"),
                    self.define("XEUS_BUILD_TESTS", self.run_tests),
                    self.define("XEUS_DOWNLOAD_GTEST", self.run_tests),
                ]
            )

        return args
