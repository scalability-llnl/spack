# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psrcat(MakefilePackage):
    """ATNF Pulsar Catalogue
    A catalogue of pulsars provided by the Australian Telescope National
    Facility"""

    homepage = "https://www.atnf.csiro.au/research/pulsar/psrcat/"
    url = "https://www.atnf.csiro.au/research/pulsar/psrcat/downloads/psrcat_pkg.v1.68.tar.gz"

    version("1.68", sha256="fbe4710c9122e4f93dbca54cf42cc2906f948f76885b241d1da2f8caecfbc657")

    depends_on("c", type="build")  # generated

    def build(self, spec, prefix):
        makeit = which("./makeit")
        makeit()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("psrcat", prefix.bin)
