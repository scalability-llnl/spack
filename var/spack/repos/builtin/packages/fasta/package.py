# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fasta(MakefilePackage):
    """The FASTA programs find regions of local or global similarity
    between Protein or DNA sequences, either by searching Protein or
    DNA databases, or by identifying local duplications within a
    sequence. Other programs provide information on the statistical
    significance of an alignment. Like BLAST, FASTA can be used to
    infer functional and evolutionary relationships between sequences
    as well as help identify members of gene families.
    """

    homepage = "https://fasta.bioch.virginia.edu/fasta_www2/fasta_list2.shtml"
    url = "https://github.com/wrpearson/fasta36/archive/fasta-v36.3.8g.tar.gz"

    license("Apache-2.0")

    version("36.3.8g", sha256="fa5318b6f8d6a3cfdef0d29de530eb005bfd3ca05835faa6ad63663f8dce7b2e")
    version(
        "36.3.8h_2020-05-04",
        sha256="d13ec06a040e4d77bf6913af44b705d3ecc921131da018e71d24daf47d3664d3",
        url="https://github.com/wrpearson/fasta36/archive/refs/tags/v36.3.8h_04-May-2020.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    # The src tree includes a plethora of variant Makefiles and the
    # builder is expected to choose one that's appropriate.  This'll
    # do for a first cut.  I can't test anything else....
    @property
    def makefile_name(self):
        if self.spec.satisfies("platform=darwin"):
            name = "Makefile.os_x86_64"
        elif self.spec.satisfies("platform=linux target=x86_64:"):
            name = "Makefile.linux64_sse2"
        else:
            tty.die(
                """Unsupported platform/target, must be
Darwin (assumes 64-bit)
Linux x86_64
"""
            )
        return name

    @property
    def makefile_path(self):
        return join_path(self.stage.source_path, "make", self.makefile_name)

    def edit(self, spec, prefix):
        makefile = FileFilter(self.makefile_path)
        makefile.filter("XDIR = .*", "XDIR = {0}".format(prefix.bin))

    def build(self, spec, prefix):
        with working_dir("src"):
            make("-f", self.makefile_path)

    def install(self, spec, prefix):
        with working_dir("src"):
            mkdir(prefix.bin)
            make("-f", self.makefile_path, "install")
