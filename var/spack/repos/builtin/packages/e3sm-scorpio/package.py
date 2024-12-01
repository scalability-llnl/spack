# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E3smScorpio(CMakePackage):
    """The SCORPIO (Software for Caching Output and Reads for Parallel I/O)
    library is used by all the model components in DOE's Energy Exascale Earth
    System Model (E3SM) for reading input data and writing model output"""

    homepage = "https://e3sm.org/scorpio-parallel-io-library/"
    url = "https://github.com/E3SM-Project/scorpio/archive/refs/tags/scorpio-v1.4.1.tar.gz"

    version("1.4.1", sha256="7cb4589410080d7e547ef17ddabe68f749e6af019c1d0e6ee9f11554f3ff6b1a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("timing", default=False, description="Enable timing")
    variant("mpi", default=True, description="Enable MPI")

    depends_on("gptl", when="+timing")
    depends_on("mpi", when="+mpi")
    depends_on("parallel-netcdf", when="+mpi")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")

    def cmake_args(self):
        opts = []
        opts.append(self.define("NetCDF_C_PATH", self.spec["netcdf-c"].prefix))
        opts.append(self.define("NetCDF_Fortran_PATH", self.spec["netcdf-fortran"].prefix))

        if self.spec.satisfies("+timing"):
            opts.append(self.define("PIO_ENABLE_TIMING", "ON"))
            opts.append(self.define("GPTL_PATH", self.spec["gptl"].prefix))
        else:
            opts.append(self.define("PIO_ENABLE_TIMING", "OFF"))

        if self.spec.satisfies("+mpi"):
            opts.append(self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc))
            opts.append(self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx))
            opts.append(self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc))
            opts.append(self.define("WITH_PNETCDF", "ON"))
            opts.append(self.define("PNETCDF_PATH", self.spec["parallel-netcdf"].prefix))
        else:
            opts.append(self.define("WITH_PNETCDF", "OFF"))

        return opts

    def setup_build_environment(self, env):
        env.set("NetCDF_C_PATH", self.spec["netcdf-c"].prefix)
        env.set("NetCDF_Fortran_PATH", self.spec["netcdf-fortran"].prefix)
        if self.spec.satisfies("+mpi"):
            env.set("PNETCDF_PATH", self.spec["parallel-netcdf"].prefix)
