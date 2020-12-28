# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Variorum(CMakePackage):
    """Variorum is a library providing vendor-neutral interfaces for
       monitoring and controlling underlying hardware features.
    """

    homepage = "https://variorum.readthedocs.io"
    git = "https://github.com/llnl/variorum.git"
    url = "https://github.com/llnl/variorum/archive/v0.1.0.tar.gz"

    maintainers = ["slabasan", "rountree"]

    version("0.1.0", tag="v0.1.0")

    ############
    # Variants #
    ############
    variant("shared", default=True, description="Build Variorum as shared lib")
    variant("docs", default=False,
            description="Build Variorum's documentation")
    variant("log", default=False, description="Enable Variorum's logs")
    variant("build_type", default="Release",
            description="CMake build type",
            values=("Debug", "Release"))

    ########################
    # Package dependencies #
    ########################
    depends_on("cmake@2.8:", type="build")
    depends_on("hwloc@1.11.9")

    #########################
    # Documentation related #
    #########################
    depends_on("py-sphinx", when="+docs", type="build")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if "+shared" in spec:
            cmake_args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            cmake_args.append("-DBUILD_SHARED_LIBS=OFF")

        if "+docs" in spec:
            cmake_args.append("-DBUILD_DOCS=ON")
            sphinx_build_exe = join_path(
                spec["py-sphinx"].prefix.bin,
                "sphinx-build"
            )
            cmake_args.append("-DSPHINX_EXECUTABLE=" + sphinx_build_exe)
        else:
            cmake_args.append("-DBUILD_DOCS=OFF")

        if 'build_type=Debug' in spec:
            cmake_args.append("-DVARIORUM_DEBUG=ON")
        else:
            cmake_args.append("-DVARIORUM_DEBUG=OFF")

        if "+log" in spec:
            cmake_args.append("-DVARIORUM_LOG=ON")
        else:
            cmake_args.append("-DVARIORUM_LOG=OFF")

        if self.run_tests:
            cmake_args.append("-DBUILD_TESTS=ON")
        else:
            cmake_args.append("-DBUILD_TESTS=OFF")

        return cmake_args
