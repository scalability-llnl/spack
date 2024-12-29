# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Coevp(MakefilePackage):
    """CoEVP is a scale-bridging proxy application for embedded viscoplasticity
    applications. It is created and maintained by The Exascale Co-Design Center
    for Materials in Extreme Environments (ExMatEx). The code is intended to
    serve as a vehicle for co-design by allowing others to extend and/or
    reimplement it as needed to test performance of new architectures,
    programming models, etc.
    Due to the size and complexity of the studied models, as well as
    restrictions on distribution, the currently available LULESH proxy
    application provides the coarse-scale model implementation and the ASPA
    proxy application provides the adaptive sampling support."""

    homepage = "https://github.com/exmatex/CoEVP"
    git = "https://github.com/exmatex/CoEVP.git"

    version("develop", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI Support")
    variant("silo", default=False, description="Build with silo Support")
    variant("flann", default=False, description="Build with flann Support")

    depends_on("mpi", when="+mpi")
    depends_on("silo", when="+silo")
    depends_on("flann@1.8.1", when="+flann")
    depends_on("lapack")

    tags = ["proxy-app"]

    @property
    def build_targets(self):
        targets = []
        if self.spec.satisfies("+mpi"):
            targets.append("COEVP_MPI=yes")
        else:
            targets.append("COEVP_MPI=no")
        if self.spec.satisfies("+flann"):
            targets.append("FLANN=yes")
            targets.append("FLANN_TARGET=")
            targets.append(
                "FLANN_LOC={0}".format(join_path(self.spec["flann"].prefix.include, "flann"))
            )
        else:
            targets.append("FLANN=no")
        targets.append("REDIS=no")
        if self.spec.satisfies("+silo"):
            targets.append("SILO=yes")
            targets.append("SILO_TARGET=")
            targets.append("SILO_LOC={0}".format(self.spec["silo"].prefix))
        else:
            targets.append("SILO=no")
        targets.append("TWEMPROXY=no")
        targets.append("LAPACK=%s" % self.spec["lapack"].libs.ld_flags)

        return targets

    def edit(self, spec, prefix):
        # libquadmath is only available x86_64 and powerle
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85440
        if self.spec.target.family not in ["x86_64", "ppc64le"]:
            comps = join_path("LULESH", "Makefile")
            filter_file("-lquadmath", "", comps)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install("LULESH/lulesh", prefix.bin)
        install("COPYRIGHT", prefix.doc)
        install("README.md", prefix.doc)
        install("CoEVP.pdf", prefix.doc)
