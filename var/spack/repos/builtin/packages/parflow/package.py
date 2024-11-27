# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parflow(CMakePackage):
    """ParFlow is an open-source parallel watershed simulator which
    includes overland flow, complex topology, heterogeneity and coupled
    land-surface processes."""

    homepage = "https://www.parflow.org/"
    url = "https://github.com/parflow/parflow/archive/v3.9.0.tar.gz"
    git = "https://github.com/parflow/parflow.git"

    maintainers("smithsg84")

    version("develop", branch="master")
    version("3.9.0", sha256="0ac610208baf973ac07ca93187ec289ba3f6e904d3f01d721ee96a2ace0f5e48")
    version("3.8.0", sha256="5ad01457bb03265d1e221090450e3bac5a680d6290db7e3872c295ce6d6aaa08")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")

    # Using explicit versions to keep builds consistent
    depends_on("tcl@8.6.11")
    depends_on("mpi@3.0.0", when="+mpi")
    depends_on("hdf5@1.10.7 +mpi", when="+mpi")
    depends_on("netcdf-c@4.5.0")
    depends_on("silo@4.10.2 -hzip -fpzip")
    depends_on("hypre@2.20.0")

    parallel = False

    def cmake_args(self):
        """Populate cmake arguments for ParFlow."""
        spec = self.spec

        cmake_args = [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DPARFLOW_AMPS_LAYER=mpi1",
            "-DPARFLOW_HAVE_CLM=TRUE",
            "-DTCL_TCLSH={0}".format(spec["tcl"].prefix.bin.tclsh),
            "-DTCL_LIBRARY={0}".format(
                LibraryList(
                    find_libraries("libtcl*", self.spec["tcl"].prefix, shared=True, recursive=True)
                )
            ),
            "-DHDF5_ROOT={0}".format(spec["hdf5"].prefix),
            "-DSILO_ROOT={0}".format(spec["silo"].prefix),
            "-DHYPRE_ROOT={0}".format(spec["hypre"].prefix),
            "-DPARFLOW_ENABLE_NETCDF=TRUE",
            "-DNETCDF_DIR={0}".format(spec["netcdf-c"].prefix),
        ]

        return cmake_args

    def setup_run_environment(self, env):
        """Setup the run environment for ParFlow package."""
        # ParFlow requires a PARFLOW_DIR env variable for correct execution
        env.set("PARFLOW_DIR", self.spec.prefix)

    examples_dir = "examples"

    def test_single_phase_flow(self):
        """Run the single phase flow test"""
        run_path = join_path(self.spec.prefix, self.examples_dir)
        options = ["default_single.tcl", "1", "1" "1"]
        with working_dir(run_path):
            exe = which(f"{self.spec['tcl'].prefix.bin}/tclsh")
            exe(*options)

    def test_check_version(self):
        """Test if exe executes"""
        exe = which(join_path(self.prefix.bin, "parflow"))
        out = exe("-v", output=str.split, error=str.split)
        assert str(self.spec.version) in out
