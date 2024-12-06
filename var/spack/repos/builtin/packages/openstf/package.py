# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openstf(MakefilePackage):
    """OpenSTF is an electrostatic field simulator which can calculate
    the voltage distribution and the electric field distribution of
    a system consisting of electrodes and dielectrics."""

    homepage = "http://www.e-em.co.jp/OpenSTF/"
    url = "http://www.e-em.co.jp/OpenSTF/OpenSTF.zip"

    version("1.7.0", sha256="50a0406dd452e3ec09d29aa362a426ca04c8a586d817ab1295988f578baeac2a")
    version(
        "1.3.1",
        sha256="4c39c81f70e3f8017fcb9cd457436c77d29e016d78bc5337f152f2eb078aa7b6",
        url="http://www.e-em.co.jp/OpenSTF/old/OpenSTF_131.zip",
    )

    variant("mpi", default=False, description="Build with MPI Support")

    depends_on("mpi", when="+mpi")

    def edit(self, spec, prefix):
        if "%gcc" in self.spec:
            filter_file("gcc", spack_cc, "./src/Makefile_gcc")
            filter_file("^LIBS.*=", "LIBS = -lm", "./src/Makefile_gcc")
            if "+mpi" in self.spec:
                filter_file("mpicc", spec["mpi"].mpicc, "./mpi/Makefile_gcc")
                filter_file("^LIBS.*=", "LIBS = -lm", "./mpi/Makefile_gcc")

        elif "%fj" in self.spec:
            filter_file("gcc", spack_cc, "./src/Makefile_gcc")
            if "+mpi" in self.spec:
                filter_file("mpicc", spec["mpi"].mpicc, "./mpi/Makefile_gcc")
                filter_file("^LIBS.*=", "LIBS = -lm", "./mpi/Makefile_gcc")

    # Openstf has "Makefile" and "Makefile_gcc".
    # "Makefile" is used only in Windows development environment.
    # The build in Windows development environment is not confirmed.
    def build(self, spec, prefix):
        with working_dir("src"):
            if "%gcc" in self.spec:
                make("-f", "Makefile_gcc")
            elif "%fj" in self.spec:
                make("-f", "Makefile_gcc")
            else:
                make()

        # To make an executable file for mpi needs object files
        # which are made for an executable file not for mpi.
        # Therefore, the build in the "src" directory is necessary
        # for to make an executable file for mpi.
        if "+mpi" in self.spec:
            with working_dir("mpi"):
                if "%gcc" in self.spec:
                    make("-f", "Makefile_gcc")
                elif "%fj" in self.spec:
                    make("-f", "Makefile_gcc")
                else:
                    make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ost", prefix.bin)
        if "+mpi" in self.spec:
            install("ost_mpi", prefix.bin)
