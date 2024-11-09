# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Simplemoc(MakefilePackage):
    """The purpose of this mini-app is to demonstrate the performance
    characterterics and viability of the Method of Characteristics (MOC)
    for 3D neutron transport calculations in the context of full scale
    light water reactor simulation."""

    homepage = "https://github.com/ANL-CESAR/SimpleMOC/"
    url = "https://github.com/ANL-CESAR/SimpleMOC/archive/v4.tar.gz"

    license("MIT")

    version("4", sha256="a39906014fdb234c43bf26e1919bdc8a13097788812e0b353a492b8e568816a6")

    depends_on("c", type="build")  # generated

    tags = ["proxy-app"]

    variant("mpi", default=True, description="Build with MPI support")

    depends_on("mpi", when="+mpi")

    build_directory = "src"

    @property
    def build_targets(self):
        targets = []

        cflags = "-std=gnu99"
        ldflags = "-lm"

        if self.compiler.name == "gcc" or self.compiler.name == "intel":
            cflags += " " + self.compiler.openmp_flag
        if "+mpi" in self.spec:
            targets.append("CC={0}".format(self.spec["mpi"].mpicc))

        targets.append("CFLAGS={0}".format(cflags))
        targets.append("LDFLAGS={0}".format(ldflags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("src/SimpleMOC", prefix.bin)
