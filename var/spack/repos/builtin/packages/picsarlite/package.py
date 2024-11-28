# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Picsarlite(MakefilePackage):
    """PICSARlite is a self-contained proxy that adequately portrays the
    computational loads and dataflow of more complex PIC codes.
    """

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://picsar.net"
    git = "https://bitbucket.org/berkeleylab/picsar.git"

    license("BSD-3-Clause-LBNL")

    version("develop", branch="PICSARlite")
    version("0.1", tag="PICSARlite-0.1", commit="3c9cee9bdf32da0998f504bff7af31fcae2f0452")

    depends_on("c", type="build")  # generated
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

        return targets

    def build(self, spec, prefix):
        with working_dir("PICSARlite"):
            make(parallel=False, *self.build_targets)

    def install(self, spec, prefix):
        mkdirp(prefix.docs)
        install("PICSARlite/README.md", prefix.docs)

        mkdirp(prefix.bin)
        install("PICSARlite/bin/picsar", prefix.bin)
