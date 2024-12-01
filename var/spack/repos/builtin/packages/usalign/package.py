# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Usalign(Package):
    """US-align (Universal Structural alignment) is a unified protocol
    to compare 3D structures of different macromolecules (proteins,
    RNAs and DNAs) in different forms (monomers, oligomers and
    heterocomplexes) for both pairwise and multiple structure
    alignments."""

    homepage = "https://zhanggroup.org/US-align"
    # this group prefers to distribute their software as single
    # source files without any actual versioning.
    # as such this recipe will likely need updating any time
    # they update the source, with the old version being
    # deprecated.
    url = "https://zhanggroup.org/US-align/bin/module/USalign.cpp"

    maintainers("snehring")

    # date assumed from paper publication date
    version(
        "20220829",
        sha256="fdc447a0c48813f91cf3045b9c19bd0c6b98fc6a3ad23780ef75fac8d4662e8c",
        expand=False,
    )

    variant("fast-math", default=False, description="Enable fast math")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        cxx = Executable(self.compiler.cxx)
        args = ["-O3"]
        if spec.satisfies("+fast-math"):
            args.append("-ffast-math")
        args.extend(["-lm", "-o", "USalign", "USalign.cpp"])
        cxx(*args)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("USalign", prefix.bin)
