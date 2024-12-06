# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libristra(CMakePackage):
    """The ristra library is a set of support utilities for
    ristra codes, including simple mathematical operations, physical
    units, and input parsing
    """

    homepage = "https://github.com/laristra/libristra"
    url = "https://github.com/laristra/libristra/archive/master.zip"
    git = "https://github.com/laristra/libristra.git"

    version("master", branch="master", submodules=False, preferred=True)
    version("1.0.0", commit="33235fe0334ca7f1f99b386a90932d9f8e1e71de")

    depends_on("cxx", type="build")  # generated

    variant("paraview", default=False, description="Enable ParaView")
    variant("shared_lua", default=False, description="Build with shared lua")

    depends_on("cmake@3.12:")
    depends_on("mpi")
    depends_on("boost@1.70.0: cxxstd=17 +program_options")
    depends_on("lua@5.3.5:~shared", when="~shared_lua")
    depends_on("lua@5.3.5:+shared", when="+shared_lua")
    # TODO: might want to move paraview out of libristra
    depends_on("paraview", when="+paraview")
    # We explicitly depend on gtest and can no longer rely on others for it
    depends_on("googletest@1.8.1+gmock")

    def cmake_args(self):
        options = ["-DENABLE_LUA=ON"]

        options.append(self.define("ENABLE_UNIT_TESTS", self.run_tests))

        return options
