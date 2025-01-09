# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chatterbug(MakefilePackage):
    """A suite of communication-intensive proxy applications that mimic
    commonly found communication patterns in HPC codes. These codes can be
    used as synthetic codes for benchmarking, or for trace generation using
    Score-P / OTF2.
    """

    tags = ["proxy-app"]

    homepage = "https://github.com/hpcgroup/chatterbug"
    git = "https://github.com/hpcgroup/chatterbug.git"

    license("MIT")

    version("develop", branch="master")
    version("1.0", tag="v1.0", commit="ee1b13c634943dbe32ac22f5e2154b00eab8c574")

    depends_on("cxx", type="build")  # generated

    variant("scorep", default=False, description="Build with Score-P tracing")

    depends_on("mpi")
    depends_on("scorep", when="+scorep")

    @property
    def build_targets(self):
        targets = []

        targets.append("MPICXX = {0}".format(self.spec["mpi"].mpicxx))

        return targets

    def build(self, spec, prefix):
        if spec.satisfies("+scorep"):
            make("WITH_OTF2=YES")
        else:
            make()

    def install(self, spec, prefix):
        if spec.satisfies("+scorep"):
            make("WITH_OTF2=YES", "PREFIX=" + spec.prefix, "install")
        else:
            make("PREFIX=" + spec.prefix, "install")
