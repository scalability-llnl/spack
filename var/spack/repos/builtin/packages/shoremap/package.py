# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shoremap(MakefilePackage):
    """SHOREmap is a computational tool implementing a method that enables
    simple and straightforward mapping-by-sequencing analysis.

    Whole genome resequencing of pools of recombinant mutant genomes allows
    directly linking phenotypic traits to causal mutations. Such an
    analysis, called mapping-by-sequencing, combines classical genetic
    mapping and next generation sequencing by relying on selection-induced
    patterns within genome-wide allele frequency in pooled genomes."""

    homepage = "http://bioinfo.mpipz.mpg.de/shoremap/"
    url = "http://bioinfo.mpipz.mpg.de/shoremap/SHOREmap_v3.6.tar.gz"

    license("GPL-3.0-or-later")

    version("3.6", sha256="0da4179e92cbc68434a9d8eff7bd5fff55c89fd9a543a2db6bd0f69074f2ec70")

    depends_on("cxx", type="build")  # generated

    depends_on("dislin")

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter(r"-L/usr/lib/", self.spec["libxt"].libs.search_flags)
        makefile.filter(r"-L\./dislin.* -ldislin_d", self.spec["dislin:d"].libs.ld_flags)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("SHOREmap", prefix.bin)
