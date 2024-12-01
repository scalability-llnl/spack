# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mapsplice2(MakefilePackage):
    """MapSplice is a software for mapping RNA-seq data to reference genome
    for splice junction discovery that depends only on reference genome,
    and not on any further annotations."""

    homepage = "http://www.netlab.uky.edu/p/bioinfo/MapSplice2"
    url = "https://protocols.netlab.uky.edu/~zeng/MapSplice-v2.2.1.zip"

    version("2.2.1", sha256="4f3c1cb49ba0abcfc952de5946ee0b56db28c51f4f4d4f5abca66b4461ca7d05")

    patch("Makefile.patch")
    patch("mapsplice_ebwt.patch")

    depends_on("bowtie")
    depends_on("ncurses", type="link")
    depends_on("samtools", type="link")
    depends_on("python", type="run")

    def edit(self, spec, prefix):
        for iscan in find(
            "src",
            ["SamRec.*", "AlignmentHandler.cpp", "JunctionHandler.cpp", "FusionSamRec.*"],
            recursive=True,
        ):
            m = FileFilter(iscan)
            m.filter(r"iscanonical", "iscanonical2")

        for makefile in find(".", "[Mm]akefile", recursive=True):
            m = FileFilter(makefile)
            m.filter("g++", "{0}".format(spack_cxx), string=True)
            m.filter(r"CC =.*", "CC = {0}".format(spack_cc))
            m.filter(r"CPP =.*", "CPP = {0}".format(spack_cxx))
            m.filter(r"CXX =.*", "CXX = {0}".format(spack_cxx))

    def install(self, spec, prefix):
        install("mapsplice.py", prefix)
        install_tree("bin", prefix.bin)
