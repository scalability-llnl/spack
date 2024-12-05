# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GsiNcdiag(CMakePackage):
    """GSI NetCDF Diagnostics Library and Utility Tools"""

    homepage = "https://github.com/NOAA-EMC/GSI-ncdiag"
    url = "https://github.com/NOAA-EMC/GSI-ncdiag/archive/refs/tags/v1.1.1.tar.gz"

    maintainers("ulmononian")

    version("1.1.2", sha256="085884106be1f8fd94a70292102e9351c0efdf1e619a233831fafcd9ed32cd99")
    version("1.1.1", sha256="26fc10cf448dd62daa1385e38921d338778416342956c478337e6c6d1b20bf8c")
    version("1.1.0", sha256="9195801301209d6f93890944d58ffee4e24a4e35502ab27560a8c440ee53df4c")
    version("1.0.0", sha256="7251d6139c2bc1580db5f7f019e10a4c73d188ddd52ccf21ecc9e39d50a6af51")

    depends_on("fortran", type="build")  # generated

    variant("serial", default=True, description="Enable Serial NetCDF diagnostics")

    depends_on("mpi")
    depends_on("netcdf-fortran@4.5.2:")

    def cmake_args(self):
        args = [self.define_from_variant("ENABLE_NCDIAG_SERIAL", "serial")]

        args.append(self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc))
        args.append(self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc))

        return args
