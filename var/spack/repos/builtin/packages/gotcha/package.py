# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gotcha(CMakePackage):
    """C software library for shared library function wrapping,
    enables tools to intercept calls into shared libraries"""

    homepage = "https://github.com/LLNL/gotcha"
    git = "https://github.com/LLNL/gotcha.git"
    maintainers("hariharan-devarajan")
    tags = ["e4s"]

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.0.7", tag="1.0.7", commit="ae053b77e6b2800188e2c4ddd17057c9b15f4adb")
    version("1.0.6", tag="1.0.6", commit="81401b939c23562728a27d7678505090463e5c03")
    version("1.0.5", tag="1.0.5", commit="e28f10c45a0cda0e1ec225eaea6abfe72c8353aa")
    version("1.0.4", tag="1.0.4", commit="46f2aaedc885f140a3f31a17b9b9a9d171f3d6f0")
    version("1.0.3", tag="1.0.3", commit="1aafd1e30d46ce4e6555c8a4ea5f5edf6a5eade5")
    version("1.0.2", tag="1.0.2", commit="bed1b7c716ebb0604b3e063121649b5611640f25")
    version("0.0.2", tag="0.0.2", commit="c82f74778f7cae958a1bf21926d34fc910613d19")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("test", default=False, description="Build tests for Gotcha")
    patch(
        "https://github.com/LLNL/GOTCHA/commit/e82b4a1ecb634075d8f5334b796c888c86da0427.patch?full_index=1",
        sha256="3f05e61b00a1cd53ebc489e9ca5dc70b9767068bba30dba973cdbef9b14774e6",
        when="@0.0.2:1.0.2",
    )

    def configure_args(self):
        return [self.define_from_variant("GOTCHA_ENABLE_TESTS", "test")]
