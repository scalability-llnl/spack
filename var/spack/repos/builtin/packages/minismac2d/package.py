# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Minismac2d(MakefilePackage):
    """Proxy Application. Solves the finite-differenced 2D incompressible
    Navier-Stokes equations with Spalart-Allmaras one-equation
    turbulence model on a structured body conforming grid.
    """

    homepage = "https://mantevo.org"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/MiniSMAC2D/miniSMAC2D-2.0.tgz"

    tags = ["proxy-app"]

    version("2.0", sha256="ec01b74c06a2c0386efbbb61b14305327342a08fb92bf52e76f60a2063adf065")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    parallel = False

    @property
    def build_targets(self):
        targets = [
            "CPP=cpp",
            "FC={0}".format(self.spec["mpi"].mpifc),
            "LD={0}".format(self.spec["mpi"].mpifc),
            "MPIDIR=-I{0}".format(self.spec["mpi"].headers.directories[0]),
            "CPPFLAGS=-P -traditional  -DD_PRECISION",
            "FFLAGS=-O3 -c -g -DD_PRECISION",
            "LDFLAGS=-O3",
            "--file=Makefile_mpi_only",
        ]

        return targets

    def edit(self, spec, prefix):
        # Editing input file to point to installed data files
        param_file = FileFilter("smac2d.in")
        param_file.filter("bcmain_directory=.*", "bcmain_directory='.'")
        param_file.filter("bcmain_filename=.*", "bcmain_filename='bcmain.dat_original_119x31'")
        param_file.filter("xygrid_directory=.*", "xygrid_directory='.'")
        param_file.filter("xygrid_filename=.*", "xygrid_filename='xy.dat_original_119x31'")

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("smac2d_mpi_only", prefix.bin)
        install("bcmain.dat_original_119x31", prefix.bin)
        install("xy.dat_original_119x31", prefix.bin)
        install("smac2d.in", prefix.bin)
        install("README.txt", prefix.doc)
