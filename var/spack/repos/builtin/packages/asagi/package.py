# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Author: Gilbert Brietzke
# Date: July 2, 2019


class Asagi(CMakePackage):
    """a pArallel Server for Adaptive GeoInformation."""

    homepage = "https://github.com/TUM-I5/ASAGI"
    git = "https://github.com/TUM-I5/ASAGI.git"

    license("LGPL-3.0-only")

    # fetching the package via git with submodules
    # is preferred to satisfy internal-dependencies
    version("1.0.1", commit="f633f96931ae00805f599078d5a1a6a830881554", submodules=True)
    # fetching the package via git with submodules
    # is preferred to satisfy internal-dependencies
    version("1.0", commit="f67250798b435c308b9a1e7516f916f7855534ec", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "link_type",
        default="shared",
        description="build shared and/or static libraries",
        values=("static", "shared"),
        multi=True,
    )

    variant("fortran", default=True, description="enable fortran support")
    variant("max_dimensions", default=4, description="max. number of dimensions supported")
    variant("numa", default=True, description="enable NUMA support")
    variant("mpi", default=True, description="enable MPI")
    variant("threadsafe", default=True, description="enable threadsafe ASAGI-functions")
    variant("threadsafe_counter", default=False, description="enable threadsafe access counters")
    variant("threadsafe_mpi", default=True, description="make MPI calls threadsafe")
    variant("mpi3", default=True, description="enable MPI-3 (enables additional features)")
    variant("tests", default=False, description="compile tests")
    variant("examples", default=False, description="compile examples")

    depends_on("mpi", when="+mpi")
    depends_on("mpi@3:", when="+mpi3")
    depends_on("netcdf-c +mpi", when="+mpi")
    depends_on("netcdf-c ~mpi", when="~mpi")
    depends_on("numactl", when="+numa")

    conflicts("%gcc@5:", when="@:1.0.0")

    def cmake_args(self):
        link_type = self.spec.variants["link_type"].value
        spec = self.spec
        args = [
            "-DMAX_DIMENSIONS=" + spec.variants["max_dimensions"].value,
            "-DSHARED_LIB=" + ("ON" if "shared" in link_type else "OFF"),
            "-DSTATIC_LIB=" + ("ON" if "static" in link_type else "OFF"),
            self.define_from_variant("FORTRAN_SUPPORT", "fortran"),
            self.define_from_variant("THREADSAFE", "threadsafe"),
            "-DNOMPI=" + ("ON" if "~mpi" in spec else "OFF"),
            self.define_from_variant("MPI3", "mpi3"),
            "-DNONUMA=" + ("ON" if "~numa" in spec else "OFF"),
            self.define_from_variant("TESTS", "tests"),
            self.define_from_variant("EXAMPLES", "examples"),
            self.define_from_variant("THREADSAFE_COUNTER", "threadsafe_counter"),
            self.define_from_variant("THREADSAFE_MPI", "threadsafe_mpi"),
        ]
        return args
