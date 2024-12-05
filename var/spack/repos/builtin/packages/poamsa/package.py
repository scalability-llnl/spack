# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Poamsa(MakefilePackage):
    """POA is Partial Order Alignment, a fast program for multiple sequence
    alignment in bioinformatics. Its advantages are speed, scalability,
    sensitivity, and the superior ability to handle branching / indels
    in the alignment."""

    homepage = "https://sourceforge.net/projects/poamsa/"
    url = "https://downloads.sourceforge.net/project/poamsa/poamsa/2.0/poaV2.tar.gz"

    version("2.0", sha256="d98d8251af558f442d909a6527694825ef6f79881b7636cad4925792559092c2")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/poamsa/poamsa/{0}/poaV{1}.tar.gz"
        return url.format(version.dotted, version.up_to(1))

    def edit(self, spec, prefix):
        filter_file(r"^(char \*Program_name;)", "extern \\1", "black_flag.h")
        filter_file(r"^(char \*Program_version;)", "extern \\1", "black_flag.h")

    def build(self, spec, prefix):
        make("poa")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        install("poa", prefix.bin)
        install("liblpo.a", prefix.lib)
