# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AtomDft(MakefilePackage):
    """ATOM is a program for DFT calculations in atoms and pseudopotential
    generation."""

    homepage = "https://departments.icmab.es/leem/siesta/Pseudopotentials/"
    url = "https://departments.icmab.es/leem/siesta/Pseudopotentials/Code/atom-4.2.6.tgz"

    version("4.2.6", sha256="489f0d883af35525647a8b8f691e7845c92fe6b5a25b13e1ed368edfd0391ed2")

    depends_on("libgridxc")
    depends_on("xmlf90")

    def edit(self, spec, prefix):
        copy("arch.make.sample", "arch.make")

    @property
    def build_targets(self):
        return [
            f"XMLF90_ROOT={self.spec['xmlf90'].prefix}",
            f"GRIDXC_ROOT={self.spec['libgridxc'].prefix}",
            "FC=fc",
        ]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("atm", prefix.bin)
