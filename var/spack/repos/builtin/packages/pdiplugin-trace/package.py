# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *


class PdipluginTrace(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("develop", branch="main", no_cache=True)
    version("1.8.1", commit="105161d5c93431d674c73ef365dce3eb724b4fcb")
    version("1.8.0", commit="edce72fc198475bab1541cc0b77a30ad02da91c5")
    version("1.7.1", commit="7eadb5314eae65fa08010bb0d35a4dcace0ebb48")
    version("1.6.0", commit="92da1ee7fc77dce6614de49ec10d991b14e7fd02")
    version("1.5.5", commit="43bd8fdae3bd12a950ff68b09d22cd74923f4eb1")
    version("1.4.3", commit="0e92542d1df70918712cb5ee378bd6ad1199ba2d")
    version("1.3.1", commit="6a075a7af3383d1d5a6278017760b6d3dc746517")
    version("1.2.2", commit="4f7076d6e45ba3feead63a7d710695def52b8380")
    version("1.1.0", commit="5cd945d28d600d54949f610e4c152a59171b2f39")

    variant("tests", default=False, description="Build tests")

    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("cmake@3.10:", type=("build"), when="@1.5:")
    depends_on("cmake@3.5:", type=("build"), when="@:1.4.3")
    depends_on("pdi@develop", type=("link", "run"), when="@develop")
    depends_on("pdi@1.8.1", type=("link", "run"), when="@1.8.1")
    depends_on("pdi@1.8.0", type=("link", "run"), when="@1.8.0")
    depends_on("pdi@1.7.1", type=("link", "run"), when="@1.7.1")
    depends_on("pdi@1.6.0", type=("link", "run"), when="@1.6.0")
    depends_on("pdi@1.5.5", type=("link", "run"), when="@1.5.5")
    depends_on("pdi@1.5.4", type=("link", "run"), when="@1.5.4")
    depends_on("pdi@1.5.3", type=("link", "run"), when="@1.5.3")
    depends_on("pdi@1.5.2", type=("link", "run"), when="@1.5.2")
    depends_on("pdi@1.5.1", type=("link", "run"), when="@1.5.1")
    depends_on("pdi@1.5.0", type=("link", "run"), when="@1.5.0")
    depends_on("pdi@1.4.3", type=("link", "run"), when="@1.4.3")
    depends_on("pdi@1.4.2", type=("link", "run"), when="@1.4.2")
    depends_on("pdi@1.4.1", type=("link", "run"), when="@1.4.1")
    depends_on("pdi@1.4.0", type=("link", "run"), when="@1.4.0")
    depends_on("pdi@1.3.1", type=("link", "run"), when="@1.3.1")
    depends_on("pdi@1.3.0", type=("link", "run"), when="@1.3.0")
    depends_on("pdi@1.2.2", type=("link", "run"), when="@1.2.2")
    depends_on("pdi@1.2.1", type=("link", "run"), when="@1.2.1")
    depends_on("pdi@1.2.0", type=("link", "run"), when="@1.2.0")
    depends_on("pdi@1.1.0", type=("link", "run"), when="@1.1.0")
    depends_on("pdi@1.0.1", type=("link", "run"), when="@1.0.1")
    depends_on("pdi@1.0.0", type=("link", "run"), when="@1.0.0")
    depends_on("pdi@0.6.5", type=("link", "run"), when="@0.6.5")
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/trace"

    def cmake_args(self):
        return [
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            "-DBUILD_TESTING:BOOL={:s}".format("ON" if "+tests" in self.spec else "OFF"),
            "-DBUILD_CFG_VALIDATOR:BOOL=OFF",
        ]

    def setup_run_environment(self, env):
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)
