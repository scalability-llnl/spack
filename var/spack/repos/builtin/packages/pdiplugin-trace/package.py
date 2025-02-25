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

    variant("tests", default=False, description="Build tests")

    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("pdi@develop", type=("link", "run"), when="@develop")
    depends_on("pdi@1.8.1", type=("link", "run"), when="@1.8.1")
    depends_on("pdi@1.8.0", type=("link", "run"), when="@1.8.0")
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
