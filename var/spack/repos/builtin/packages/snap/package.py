# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snap(MakefilePackage):
    """SNAP serves as a proxy application to model
    the performance of a modern discrete ordinates
    neutral particle transport application.
    SNAP may be considered an update to Sweep3D,
    intended for hybrid computing architectures.
    It is modeled off the Los Alamos National Laboratory code PARTISN."""

    homepage = "https://github.com/lanl/SNAP"
    git = "https://github.com/lanl/SNAP.git"

    tags = ["proxy-app"]

    license("Unlicense")

    version("master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=False, description="Build with OpenMP support")
    variant("opt", default=True, description="Build with debugging")
    variant("mpi", default=True, description="Build with MPI support")

    depends_on("mpi", when="+mpi")

    build_directory = "src"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter("Makefile")
            if "~opt" in spec:
                makefile.filter("OPT = yes", "OPT = no")
            if "~mpi" in spec:
                makefile.filter("MPI = yes", "MPI = no")
            if "~openmp" in spec:
                makefile.filter("OPENMP = yes", "OPENMP = no")
            makefile.filter("FFLAGS =.*", "FFLAGS =")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("src/gsnap", prefix.bin)
        install_tree("qasnap", prefix.qasnap)
        install("README.md", prefix)
