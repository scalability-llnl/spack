# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nekbone(Package):
    """NEK5000 emulation software called NEKbone. Nekbone captures the basic
    structure and user interface of the extensive Nek5000 software.
    Nek5000 is a high order, incompressible Navier-Stokes solver based on
    the spectral element method."""

    homepage = "https://github.com/Nek5000/Nekbone"
    git = "https://github.com/Nek5000/Nekbone.git"

    tags = ["proxy-app", "ecp-proxy-app"]

    license("mpich2")

    version("develop", branch="master")
    version(
        "17.0",
        sha256="ae361cc61368a924398a28a296f675b7f0c4a9516788a7f8fa3c09d787cdf69b",
        url="https://github.com/Nek5000/Nekbone/archive/v17.0.tar.gz",
        extension=".tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Variants
    variant("mpi", default=True, description="Build with MPI")

    # dependencies
    depends_on("mpi", when="+mpi")

    @run_before("install")
    def fortran_check(self):
        if not self.compiler.fc:
            msg = "Nekbone can not be built without a Fortran compiler."
            raise RuntimeError(msg)

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        fc = self.compiler.fc
        cc = self.compiler.cc
        if "+mpi" in spec:
            fc = spec["mpi"].mpif77
            cc = spec["mpi"].mpicc

        # Install Nekbone in prefix.bin
        install_tree(self.stage.source_path, prefix.bin.Nekbone)

        # Install scripts in prefix.bin
        nekpmpi = "test/example1/nekpmpi"
        makenek = "test/example1/makenek"

        install(makenek, prefix.bin)
        install(nekpmpi, prefix.bin)

        error = Executable(fc)("empty.f", output=str, error=str, fail_on_error=False)

        fflags = ""
        if "gfortran" in error or "GNU" in error or "gfortran" in fc:
            # Use '-std=legacy' to suppress an error that used to be a
            # warning in previous versions of gfortran.
            fflags = " -std=legacy"

        with working_dir(prefix.bin):
            filter_file(
                r"^SOURCE_ROOT\s*=.*", 'SOURCE_ROOT="' + prefix.bin.Nekbone + '/src"', "makenek"
            )
            filter_file(r"^CC\s*=.*", 'CC="' + cc + '"', "makenek")
            filter_file(r"^F77\s*=.*", 'F77="' + fc + fflags + '"', "makenek")

            if "+mpi" not in spec:
                filter_file(r"^#IFMPI=\"false\"", 'IFMPI="false"', "makenek")
