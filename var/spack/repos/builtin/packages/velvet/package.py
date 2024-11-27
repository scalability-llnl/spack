# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def is_positive_int(x):
    if x.isdigit() and int(x) > 0:
        return True
    else:
        return False


class Velvet(MakefilePackage):
    """Velvet is a de novo genomic assembler specially designed for short read
    sequencing technologies."""

    homepage = "https://www.ebi.ac.uk/~zerbino/velvet/"
    url = "https://www.ebi.ac.uk/~zerbino/velvet/velvet_1.2.10.tgz"

    maintainers("snehring")

    license("GPL-2.0-only")

    version("1.2.10", sha256="884dd488c2d12f1f89cdc530a266af5d3106965f21ab9149e8cb5c633c977640")

    variant(
        "categories",
        default="2",
        description="Number of channels which can be handled independently",
        values=is_positive_int,
    )
    variant(
        "maxkmerlength",
        default="31",
        description="Longest kmer size you can use in an analysis",
        values=is_positive_int,
    )
    variant("bigassembly", default=False, description="Allow assemblies with more than 2^31 reads")
    variant(
        "vbigassembly",
        default=False,
        description="Allow unsigned 64-bit array index values (also enables bigassembly)",
    )
    variant(
        "longsequences", default=False, description="Allow assembling contigs longer than 32kb"
    )
    variant("openmp", default=False, description="Enable multithreading")
    variant("single_cov_cat", default=False, description="Per-library coverage")

    depends_on("zlib-api")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        if spec.target.family == "aarch64":
            makefile.filter("-m64", "")
        maxkmerlength = self.spec.variants["maxkmerlength"].value
        categories = self.spec.variants["categories"].value
        makefile.filter(r"^MAXKMERLENGTH\s*=\s*.*", f"MAXKMERLENGTH = {maxkmerlength}")
        makefile.filter(r"^CATEGORIES\s*=\s*.*", f"CATEGORIES = {categories}")
        if "+bigassembly" in self.spec:
            makefile.filter("^ifdef BIGASSEMBLY", "BIGASSEMBLY=1\nifdef BIGASSEMBLY")
        if "+vbigassembly" in self.spec:
            makefile.filter("^ifdef VBIGASSEMBLY", "VBIGASSEMBLY=1\nifdef VBIGASSEMBLY")
        if "+longsequences" in self.spec:
            makefile.filter("^ifdef LONGSEQUENCES", "LONGSEQUENCES=1\nifdef LONGSEQUENCES")
        if "+openmp" in self.spec:
            makefile.filter("^ifdef OPENMP", "OPENMP=1\nifdef OPENMP")
        if "+single_cov_cat" in self.spec:
            makefile.filter("^ifdef SINGLE_COV_CAT", "SINGLE_COV_CAT=1\nifdef SINGLE_COV_CAT")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("velvetg", prefix.bin)
        install("velveth", prefix.bin)
