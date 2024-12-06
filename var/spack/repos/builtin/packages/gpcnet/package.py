# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gpcnet(MakefilePackage):
    """Global Performance and Congestion Network Test - GPCNeT."""

    homepage = "https://github.com/netbench/GPCNET"
    git = "https://github.com/netbench/GPCNET.git"

    license("Apache-2.0")

    version("master")

    depends_on("c", type="build")  # generated

    depends_on("mpi", type=("build", "run"))

    @property
    def build_targets(self):
        spec = self.spec
        return ["all", "CC={}".format(spec["mpi"].mpicc)]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("network_load_test", prefix.bin)
        install("network_test", prefix.bin)
