# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prophecy4f(MakefilePackage):
    """Prophecy4f is a Monte Carlo integrator for
    Higgs decays H -> WW/ZZ -> 4 fermions."""

    homepage = "https://prophecy4f.hepforge.org/"
    url = "https://prophecy4f.hepforge.org/downloads/?f=Prophecy4f-3.0.2.tar.gz"

    maintainers("haralmha", "vvolkl")

    tags = ["hep"]

    version("3.0.2", sha256="01e6ad4d7e913082c1dcabd589173f5d962086dd7860c710f14a0528d8d80eb7")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("collier")

    @property
    def build_targets(self):
        return [
            "COLLIERDIR={0}/lib".format(self.spec["collier"].prefix),
            "INPUT=-I{0}/include/".format(self.spec["collier"].prefix),
            "FC=gfortran",
        ]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share.prophecy4f)
        install("Prophecy4f", prefix.bin)
        install("defaultinput", prefix)
