# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5.

    Usage: Set the HDF5_VOL_CONNECTOR environment variable to enable this adaptor, i.e.

        $export HDF5_VOL_CONNECTOR="async under_vol=0;under_info={}"

    ref. https://hdf5-vol-async.readthedocs.io/en/latest/gettingstarted.html#set-environmental-variables
    """

    homepage = "https://hdf5-vol-async.readthedocs.io"
    git = "https://github.com/hpc-io/vol-async.git"

    maintainers("hyoklee", "houjun", "jeanbez")

    tags = ["e4s"]

    license("BSD-3-Clause-LBNL")

    version("develop", branch="develop")
    version("1.7", tag="v1.7", commit="70a22cf9863a7c1386d97be865342deb751ca501")
    version("1.6", tag="v1.6", commit="f3406d62ec055cdcfe077979a1068bd102c598a5")
    version("1.5", tag="v1.5", commit="b917713ffcb207d9799c6d6863cf805ee54ccfea")

    depends_on("c", type="build")  # generated

    variant("memcpy", default=False, description="Enable buffer copy for dataset write")

    depends_on("mpi")
    depends_on("argobots@1.1:")
    depends_on("hdf5@1.14.0: +mpi +threadsafe")

    # Require MPI_THREAD_MULTIPLE.
    depends_on("openmpi +thread_multiple", when="^[virtuals=mpi] openmpi@:2")
    depends_on("mvapich2 threads=multiple", when="^[virtuals=mpi] mvapich2")

    def setup_run_environment(self, env):
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
        env.set("MPICH_MAX_THREAD_SAFETY", "multiple")

    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
        args = [
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("ENABLE_WRITE_MEMCPY", "memcpy"),
        ]
        return args

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                make("test")
