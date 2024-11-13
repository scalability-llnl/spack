# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Picsar(MakefilePackage):
    """PICSAR is a high performance library of optimized versions of the key
    functionalities of the PIC loop.
    """

    homepage = "https://picsar.net"
    git = "https://bitbucket.org/berkeleylab/picsar.git"

    license("BSD-3-Clause-LBNL")

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("prod", default=True, description="Production mode (without FFTW)")
    variant(
        "prod_spectral", default=False, description="Production mode with spectral solver and FFTW"
    )
    variant("debug", default=False, description="Debug mode")
    variant("vtune", default=False, description="Vtune profiling")
    variant("sde", default=False, description="sde profiling")
    variant("map", default=False, description="Allinea Map profiling")
    variant("library", default=False, description="Create static and dynamic library")

    depends_on("mpi")
    depends_on("fftw@3.0: +mpi", when="+prod_spectral")

    parallel = False

    def patch(self):
        if "%arm" in self.spec:
            filter_file(r"!\$OMP SIMD SAFELEN\(LVEC2\)", "", "src/diags/diags.F90")

    @property
    def build_targets(self):
        targets = []
        targets.append("FC={0}".format(self.spec["mpi"].mpifc))
        targets.append("CC={0}".format(self.spec["mpi"].mpicc))

        comp = "user"
        vendors = {"%gcc": "gnu", "%intel": "intel"}
        for key, value in vendors.items():
            if self.spec.satisfies(key):
                comp = value
        targets.append("COMP={0}".format(comp))
        if comp == "user":
            targets.append("FARGS={0}{1}".format("-g -O3 ", self.compiler.openmp_flag))

        if "+prod" in self.spec:
            mode = "prod"
        elif "+prod_spectral" in self.spec:
            mode = "prod_spectral"
        elif "+debug" in self.spec:
            mode = "debug"
        elif "+vtune" in self.spec:
            mode = "vtune"
        elif "+sde" in self.spec:
            mode = "sde"
        elif "+map" in self.spec:
            mode = "map"
        elif "+library" in self.spec:
            mode = "library"
        targets.append("MODE = {0}".format(mode))

        targets.append("SYS = default")

        if "%gcc" in self.spec:
            targets.append(
                "FARGS=-g -fbounds-check -O3 -fopenmp " "-JModules -fallow-argument-mismatch"
            )

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.docs)
        install("README.md", prefix.docs)

        mkdirp(prefix.bin)
        install("fortran_bin/picsar", prefix.bin)
