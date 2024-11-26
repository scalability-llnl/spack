# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Swan(MakefilePackage):
    """SWAN is a third-generation wave model, developed at Delft
    University of Technology, that computes random, short-crested
     wind-generated waves in coastal regions and inland waters.
    For more information about SWAN, see a short overview of model
    features. This list reflects on the scientific relevance of
    the development of SWAN."""

    homepage = "https://swanmodel.sourceforge.net/"
    url = "https://swanmodel.sourceforge.io/download/zip/swan4145.tar.gz"

    maintainers("lhxone", "stevenrbrandt")

    # This is very important
    parallel = False

    version(
        "4145",
        preferred=True,
        sha256="4cced2250f11f5cff3417d1f541f5e3cdd09fa1bc4fd986e0d0917bfb88b1e2a",
    )

    version("4141", sha256="5d411e6602bd4ef764f6c7d23e5e25b588e955cb21a606d6d8a7bc4c9393aa0a")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("netcdf-fortran")
    depends_on("perl", type="build")

    def edit(self, spec, prefix):
        fc = re.sub(r".*[\\/]", "", env["FC"])
        mpifc = re.sub(r".*[\\/]", "", spec["mpi"].mpifc)

        # Must not be the full path to the compiler or platform.pl gets confused
        env["FC"] = fc
        env["F90_MPI"] = mpifc

        m = FileFilter("platform.pl")
        m.filter("F90_MPI = .*", "F90_MPI = " + mpifc + '\\n";')
        m.filter("NETCDFROOT =", "NETCDFROOT = " + spec["netcdf-fortran"].prefix)
        m.filter(r"-lnetcdf\b", "")

    def build(self, spec, prefix):
        make("config")
        make("mpi")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("*.exe", prefix.bin)
