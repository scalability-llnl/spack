# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tracer(MakefilePackage):
    """Trace Replay and Network Simulation Framework"""

    homepage = "https://tracer-codes.readthedocs.io"
    git = "https://github.com/LLNL/tracer.git"

    maintainers("bhatele")

    license("MIT")

    version("develop", branch="master")
    version("2.2", tag="v2.2", commit="fdd1b07a1a0faca14aac53dcbcbccc44237ae7cb")

    depends_on("cxx", type="build")  # generated

    variant("otf2", default=True, description="Use OTF2 traces for simulation")

    depends_on("mpi")
    depends_on("codes")
    depends_on("otf2", when="+otf2")

    build_directory = "tracer"

    @property
    def build_targets(self):
        targets = []

        targets.append("CXX = {0}".format(self.spec["mpi"].mpicxx))
        if "+otf2" in self.spec:
            targets.append("SELECT_TRACE = -DTRACER_OTF_TRACES=1")

        return targets

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("PREFIX={0}".format(prefix), "install")
