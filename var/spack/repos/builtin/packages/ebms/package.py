# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ebms(MakefilePackage):
    """This is a miniapp for the Energy Banding Monte Carlo (EBMC)
    neutron transportation simulation code.  It is adapted from a
    similar miniapp provided by Andrew Siegel, whose algorithm is
    described in [1], where only one process in a compute node
    is used, and the compute nodes are divided into memory nodes
    and tracking nodes.    Memory nodes do not participate in particle
    tracking. Obviously, there is a lot of resource waste in this design.
    """

    homepage = "https://github.com/ANL-CESAR/EBMS"
    git = "https://github.com/ANL-CESAR/EBMS.git"

    license("MIT")

    version("develop")

    depends_on("c", type="build")  # generated

    depends_on("mpi@2:")

    tags = ["proxy-app"]

    @property
    def build_targets(self):
        targets = []

        cflags = "-g -O3 -std=gnu99"

        if self.spec.satisfies("+mpi"):
            targets.append("CC={0}".format(self.spec["mpi"].mpicc))

        targets.append("CFLAGS={0}".format(cflags))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("ebmc-iallgather", prefix.bin)
        install("ebmc-rget", prefix.bin)
        install_tree("run", join_path(prefix, "run"))
        install_tree("inputs", join_path(prefix, "inputs"))
