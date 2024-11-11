# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lulesh(MakefilePackage):
    """LULESH is a highly simplified application, hard-coded to only
    style typical in scientific C or C++ based applications. Hard
    code to only solve a Sedov blast problem with analytic answer
    """

    tags = ["proxy-app"]
    homepage = "https://computing.llnl.gov/projects/co-design/lulesh"
    git = "https://github.com/LLNL/LULESH.git"

    version("2.0.3", tag="2.0.3", commit="46c2a1d6db9171f9637d79f407212e0f176e8194")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=True, description="Build with OpenMP support")
    variant("visual", default=False, description="Build with Visualization support (Silo, hdf5)")

    depends_on("mpi", when="+mpi")
    depends_on("silo", when="+visual")
    depends_on("hdf5", when="+visual")

    @property
    def build_targets(self):
        targets = []
        cxxflag = " -g -O3 -I. "
        ldflags = " -g -O3 "
        if self.spec.satisfies("~mpi"):
            targets.append("CXX = {0} {1}".format(spack_cxx, " -DUSE_MPI=0 "))
        else:
            targets.append("CXX = {0} {1}".format(self.spec["mpi"].mpicxx, " -DUSE_MPI=1"))
            targets.append("MPI_INC = {0}".format(self.spec["mpi"].prefix.include))
            targets.append("MPI_LIB = {0}".format(self.spec["mpi"].prefix.lib))
        if self.spec.satisfies("+visual"):
            targets.append("SILO_INCDIR = {0}".format(self.spec["silo"].prefix.include))
            targets.append("SILO_LIBDIR = {0}".format(self.spec["silo"].prefix.lib))
            cxxflag = " -g -DVIZ_MESH -I${SILO_INCDIR} "
            ldflags = " -g -L${SILO_LIBDIR} -Wl,-rpath=${SILO_LIBDIR} -lsiloh5 -lhdf5 "

        if self.spec.satisfies("+openmp"):
            cxxflag += self.compiler.openmp_flag
            ldflags += self.compiler.openmp_flag

        targets.append("CXXFLAGS = {0}".format(cxxflag))
        targets.append("LDFLAGS = {0}".format(ldflags))
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("lulesh{0}".format(self.version.up_to(2)), prefix.bin)
        mkdirp(prefix.doc)
        install("README", prefix.doc)
        install("TODO", prefix.doc)
