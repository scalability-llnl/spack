# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fairmq(CMakePackage):
    """C++ Message Queuing Library and Framework (https://doi.org/10.5281/zenodo.1689985)"""

    homepage = "https://github.com/FairRootGroup/FairMQ"
    git = "https://github.com/FairRootGroup/FairMQ.git"
    maintainers("dennisklein", "ChristianTackeGSI")

    license("LGPL-3.0-or-later")

    version("dev", branch="dev", submodules=True, get_full_repo=True)
    with default_args(submodules=True, no_cache=True):
        # no_cache=True is currently needed, because FairMQ's build system
        # depends on the git metadata, see also
        # https://github.com/spack/spack/issues/19972
        # https://github.com/spack/spack/issues/14344
        version("1.8.1", tag="v1.8.1", commit="961eca52761a31a0200c567b44e2b2d6d6e50df3")
        version("1.7.0", tag="v1.7.0", commit="d1c99f7e150c1177dc1cab1b2adc16475cade24e")
        version("1.6.0", tag="v1.6.0", commit="42d27af20fb5cbbbc0b0fdfef1c981d51a8baf87")
        version("1.5.0", tag="v1.5.0", commit="c8fde17b6a10a467035590fd800bb693f50c4826")

    depends_on("cxx", type="build")  # generated

    variant(
        "autobind", default=True, when="@1.7:", description="Override the channel autoBind default"
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo"),
        multi=False,
        description="CMake build type",
    )
    variant(
        "cxxstd",
        default="default",
        values=("default", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant("examples", default=False, description="Build and install usage examples.")

    generator("make", "ninja", default="ninja")

    with default_args(type="build"):
        depends_on("cmake@3.15:")
        depends_on("faircmakemodules")
        depends_on("git")

    depends_on("boost@1.66: +container+program_options+filesystem+date_time+regex")
    depends_on("fairlogger@1.6: +pretty")
    depends_on("libzmq@4.1.4:")

    def cmake_args(self):
        args = [
            self.define("DISABLE_COLOR", True),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_EXAMPLES", "examples"),
            self.define_from_variant("FAIRMQ_CHANNEL_DEFAULT_AUTOBIND", "autobind"),
        ]
        if self.spec.variants["cxxstd"].value != "default":
            args.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        return list(filter(bool, args))  # return non-falsy args
