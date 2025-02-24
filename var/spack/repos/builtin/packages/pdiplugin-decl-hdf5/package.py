# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *


class PdipluginDeclHdf5(CMakePackage):
    """Decl'HDF5 plugin enables one to read and write data from HDF5 files in a
    declarative way. Decl'HDF5 does not support the full HDF5 feature set but
    offers a simple declarative interface to access a large subset of it for the
    PDI library"""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("develop", branch="main", no_cache=True)
    version("1.8.1", commit="105161d5c93431d674c73ef365dce3eb724b4fcb")
    version("1.8.0", commit="edce72fc198475bab1541cc0b77a30ad02da91c5")

    variant("benchs", default=False, description="Build benchmarks")
    variant("fortran", default=True, description="Enable Fortran (for tests only)")
    variant("tests", default=False, description="Build tests")
    variant("mpi", default=True, description="Enable parallel HDF5")

    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("hdf5@1.10.4:1 +shared", type=("build", "link", "run"), when="@1.8:")
    depends_on("hdf5 +mpi", type=("build", "link", "run"), when="+mpi")
    depends_on("pdi@develop", type=("link", "run"), when="@develop")
    depends_on("pdi@1.8.1", type=("link", "run"), when="@1.8.1")
    depends_on("pdi@1.8.0", type=("link", "run"), when="@1.8.0")
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/decl_hdf5"

    def cmake_args(self):
        args = [
            "-DBUILD_BENCHMARKING:BOOL={:s}".format("ON" if "+benchs" in self.spec else "OFF"),
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            "-DBUILD_TESTING:BOOL={:s}".format("ON" if "+tests" in self.spec else "OFF"),
            "-DBUILD_FORTRAN:BOOL={:s}".format("ON" if "+tests" in self.spec else "OFF"),
            "-DBUILD_HDF5_PARALLEL:BOOL={:s}".format("ON" if "+mpi" in self.spec else "OFF"),
            "-DBUILD_CFG_VALIDATOR:BOOL=OFF",
        ]
        return args

    def setup_run_environment(self, env):
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)
