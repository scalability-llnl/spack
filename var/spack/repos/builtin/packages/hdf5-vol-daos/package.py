# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hdf5VolDaos(CMakePackage):
    """The HDF5 DAOS VOL connector is an external VOL connector
    that interfaces with the DAOS API"""

    homepage = "https://github.com/HDFGroup/vol-daos"
    url = (
        "https://github.com/HDFGroup/vol-daos/releases/download/v1.2.0/hdf5_vol_daos-1.2.0.tar.bz2"
    )
    git = "https://github.com/HDFGroup/vol-daos.git"

    maintainers("hyoklee", "soumagne")

    license("BSD-3-Clause")

    version("master", branch="master", submodules=True)
    version("1.2.0", sha256="669c1443605068f24c033783ef72619afcec4844902b3e0bffa19ddeea39779f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.12.2:", type="build")
    depends_on("daos@2.2.0:")
    depends_on("hdf5@1.14.0:+hl+mpi+map")

    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""
        define = self.define

        cmake_args = [
            define("BUILD_SHARED_LIBS", True),
            define("BUILD_TESTING", self.run_tests),
            define("PC_DAOS_INCLUDEDIR", self.spec["daos"].prefix + "/include"),
            define("PC_DAOS_LIBDIR", self.spec["daos"].prefix + "/lib64"),
        ]

        return cmake_args

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.prefix.lib)

    def check(self):
        """Unit tests fail when run in parallel."""

        with working_dir(self.build_directory):
            make("test", parallel=False)
