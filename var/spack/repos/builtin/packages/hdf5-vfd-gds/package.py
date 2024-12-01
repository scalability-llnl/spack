# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VfdGds(CMakePackage, CudaPackage):
    """This package enables GPU Direct Storage Virtual File Driver in HDF5."""

    # Package info
    homepage = "https://github.com/hpc-io/vfd-gds"
    url = "https://github.com/hpc-io/vfd-gds/archive/refs/tags/1.0.1.tar.gz"
    git = "https://github.com/hpc-io/vfd-gds.git"
    maintainers("hyoklee", "lrknox")

    license("BSD-3-Clause-LBNL")

    # Versions
    version("master", branch="master")
    version("1.0.2", sha256="f7df64ff62e057b525bc30ed6534f9c0752e52bd58b65f7c147878d6c68105ae")
    version("1.0.1", sha256="00e125fd149561be991f41e883824de826d8add604aebccf103a4fb82d5faac2")
    version("1.0.0", sha256="6b16105c7c49f13fc05784ee69b78d45fb159270c78d760689f9cd21e230ddd2")

    depends_on("c", type="build")  # generated

    # Dependencies
    conflicts("~cuda")
    # Although cuFILE predates 11.7.0, it is not installed in a location the build
    # system can obtaion via `find_library`.  Packaging issues fixed in 11.7.1.
    conflicts("^cuda@:11.7.0")
    depends_on("cmake@3.12:", type="build")
    depends_on("hdf5@1.14.0:")

    def cmake_args(self):
        # CMake options
        args = [self.define("BUILD_TESTING", self.run_tests)]

        return args

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
