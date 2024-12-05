# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class H5bench(CMakePackage):
    """A benchmark suite for measuring HDF5 performance."""

    homepage = "https://github.com/hpc-io/h5bench"
    git = "https://github.com/hpc-io/h5bench.git"

    maintainers("jeanbez", "sbyna")

    tags = ["e4s"]

    license("BSD-3-Clause-LBNL")

    version("latest", branch="master", submodules=True)
    version("develop", branch="develop", submodules=True)

    version("1.4", commit="67a3e6d91508e5ab77db79c6187b2eb3c96119e0", submodules=True)
    version("1.3", commit="ec75a466a77c337b4252c0afe1055c7fbe841e16", submodules=True)
    version(
        "1.2", commit="866af6777573d20740d02acc47a9080de093e4ad", submodules=True, deprecated=True
    )
    version(
        "1.1", commit="1276530a128025b83a4d9e3814a98f92876bb5c4", submodules=True, deprecated=True
    )
    version(
        "1.0", commit="9d3438c1bc66c5976279ef203bd11a8d48ade724", submodules=True, deprecated=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("metadata", default=False, when="@1.2:", description="Enables metadata benchmark")
    variant("amrex", default=False, when="@1.2:", description="Enables AMReX benchmark")
    variant("exerciser", default=False, when="@1.2:", description="Enables exerciser benchmark")
    variant("openpmd", default=False, when="@1.2:", description="Enables OpenPMD benchmark")
    variant("e3sm", default=False, when="@1.2:", description="Enables E3SM benchmark")
    variant("async", default=False, when="@1.2:", description="Enables ASYNC VOL Connector")
    variant("all", default=False, when="@1.2:", description="Enables all h5bench benchmarks")

    depends_on("cmake@3.10:", type="build")
    depends_on("mpi")
    depends_on("hdf5+mpi@1.12.0:1,develop-1.12:")
    depends_on("hdf5-vol-async@1.5", when="+async")
    depends_on("parallel-netcdf", when="+e3sm")
    depends_on("parallel-netcdf", when="+all")

    def setup_build_environment(self, env):
        env.set("HDF5_HOME", self.spec["hdf5"].prefix)

    def cmake_args(self):
        args = [
            self.define_from_variant("H5BENCH_METADATA", "metadata"),
            self.define_from_variant("H5BENCH_AMREX", "amrex"),
            self.define_from_variant("H5BENCH_EXERCISER", "exerciser"),
            self.define_from_variant("H5BENCH_OPENPMD", "openpmd"),
            self.define_from_variant("H5BENCH_E3SM", "e3sm"),
            self.define_from_variant("H5BENCH_ALL", "all"),
            self.define_from_variant("WITH_ASYNC_VOL", "async"),
        ]

        return args

    @run_after("install")
    def setup_build_tests(self):
        launcher = self.mpi_launcher()
        filename = "samples/sync-write-1d-contig-contig.json"
        filter_file("mpirun", f"{launcher}", filename)
        filter_file(r"-n 2", "-n 1 --timeout 240", filename)

        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, ["tests", "samples"])

    def mpi_launcher(self):
        commands = ["mpirun", "mpiexec"]

        return which(*commands, path=[self.spec["mpi"].prefix.bin]) or which(*commands)

    def test_help(self):
        """Run h5bench help."""
        h5bench = which(self.prefix.bin.h5bench)
        h5bench("-h")

    def test_h5bench(self):
        """Run h5bench synchronous write test."""
        with working_dir(self.test_suite.current_test_cache_dir):
            h5bench = which(self.prefix.bin.h5bench)
            h5bench("--debug", "--abort", "samples/sync-write-1d-contig-contig.json")
