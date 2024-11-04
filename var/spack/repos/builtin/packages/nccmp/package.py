# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nccmp(CMakePackage):
    """Compare NetCDF Files"""

    homepage = "https://nccmp.sourceforge.net/"
    url = "https://gitlab.com/remikz/nccmp/-/archive/1.9.0.1/nccmp-1.9.0.1.tar.gz"

    maintainers("ulmononian", "climbfuji")

    license("GPL-2.0-only")

    version("1.9.1.0", sha256="5aa8d6cbc54d26f77e3d0511690cfafa57514a4145f75e8cabce782126509c91")
    version("1.9.0.1", sha256="81e9753cf451afe8248d44c841e102349e07cde942b11d1f91b5f85feb622b99")
    version("1.8.9.0", sha256="da5d2b4dcd52aec96e7d96ba4d0e97efebbd40fe9e640535e5ee3d5cd082ae50")
    version("1.8.2.0", sha256="7f5dad4e8670568a71f79d2bcebb08d95b875506d3d5faefafe1a8b3afa14f18")

    depends_on("c", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
    depends_on("netcdf-c", type=("build", "run"))
    depends_on("mpi", when="^netcdf-c+mpi~shared")

    def cmake_args(self):
        args = []
        cflags = []

        if self.spec.satisfies("%intel"):
            cflags.append("-std=c99")

        if cflags:
            args.append(self.define("CMAKE_C_FLAGS", " ".join(cflags)))

        nc = self.spec["netcdf-c"]
        if "~shared" in nc:
            nc_flags = Executable("nc-config")("--static", "--libs", output=str).strip()
            args.append(self.define("CMAKE_EXE_LINKER_FLAGS", nc_flags))
            if "+mpi" in nc:
                args.append(self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc))

        return args
