# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openfdtd(MakefilePackage):
    """OpenFDTD is general purpose FDTD simulator applicable to a wide range
    of applications. The FDTD method (Finite Difference Time Domain method)
    is a method for numerically calculating the Maxwell equation, which is
    the basic equation of the electromagnetic field,
    by the difference method."""

    homepage = "http://www.e-em.co.jp/OpenFDTD/"
    url = "http://www.e-em.co.jp/OpenFDTD/OpenFDTD.zip"

    version("2.7.3", sha256="22171d1dd74b4e48299b0d0c69ca933aac89d4eb77c59f579af35861eaca0faa")
    version("2.7.1", sha256="3fb5fbeca3dc63243a6dc116d0f3ce3d1a854b4813f3928812ae99e07575ab1a")
    version("2.6.3", sha256="1551cce7f96c1c53ad5d5e676bce2b26fd1593dd5f492a801e976a8a65a42a00")
    version("2.6.0", sha256="92f7b92dc55ff6d8fc8c31eda77ca10fe25a5f54b002f2523a3d67f485d77e9f")
    version("2.3.0", sha256="10ac70f2ed7160da87dd9222a5a17ca7b72365ee886235359afc48c4fb7b4be4")

    variant("mpi", default=False, description="Build with MPI Support")

    depends_on("mpi", when="+mpi")

    def url_for_version(self, version):
        url = self.url
        if version < Version("2.7.3"):
            url = "http://www.e-em.co.jp/OpenFDTD/old/OpenFDTD_{0}.zip"
        return url.format(version.joined)

    def edit(self, spec, prefix):
        makefiles = [join_path("src", "Makefile_gcc")]
        if spec.satisfies("+mpi"):
            makefiles.append(join_path("mpi", "Makefile_gcc"))
        for makefile in makefiles:
            m = FileFilter(makefile)
            m.filter("gcc", spack_cc)
            m.filter("-fopenmp", self.compiler.openmp_flag)
            if spec.satisfies("+mpi"):
                m.filter("mpicc", spec["mpi"].mpicc)
            if spec.satisfies("%fj"):
                m.filter("-Ofast", "-Kfast,ocl -D_VECTOR")
                m.filter("-O2", "-Kfast,ocl -D_VECTOR")

    # Openfdtd has "Makefile" and "Makefile_gcc".
    # "Makefile" is used only in Windows development environment.
    # The build in Windows development environment is currently unsupported.
    def build(self, spec, prefix):
        with working_dir("src"):
            make("-f", "Makefile_gcc")

        # To make an executable file for mpi needs object files
        # which are made for an executable file not for mpi.
        # Therefore, the build in the "src" directory is necessary
        # for to make an executable file for mpi.
        if "+mpi" in self.spec:
            with working_dir("mpi"):
                make("-f", "Makefile_gcc")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ofd", prefix.bin)
        if "+mpi" in self.spec:
            install("ofd_mpi", prefix.bin)
