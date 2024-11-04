# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ntpoly(CMakePackage):
    """NTPoly - parallel library for computing matrix functions.

    NTPoly is a library for computing the functions of
    sparse, hermitian matrices based on polynomial expansions. For
    sufficiently sparse matrices, most of the matrix functions in
    NTPoly can be computed in linear time.
    """

    homepage = "https://william-dawson.github.io/NTPoly/"
    url = "https://github.com/william-dawson/NTPoly/archive/ntpoly-v2.3.1.tar.gz"

    license("MIT")

    version("3.1.0", sha256="71cd6827f20c68e384555dbcfc85422d0690e21d21d7b5d4f7375544a2755271")
    version("2.7.2", sha256="968571a42e93827617c40c4ceefd29be52447c176309f801bb5a454527fe5f49")
    version("2.3.1", sha256="af8c7690321607fbdee9671b9cb3acbed945148014e0541435858cf82bfd887e")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries.")

    depends_on("cmake", type="build")
    depends_on("blas", type="link")
    depends_on("mpi@3")

    def cmake_args(self):
        args = ["-DNOSWIG=Yes", self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if self.spec.satisfies("%fj"):
            args.append("-DCMAKE_Fortran_MODDIR_FLAG=-M")

        return args

    @property
    def libs(self):
        return find_libraries(
            ["libNTPoly", "libNTPolyCPP", "libNTPolyWrapper"], root=self.home, recursive=True
        )
