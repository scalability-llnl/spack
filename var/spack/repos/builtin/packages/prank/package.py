# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prank(Package):
    """A powerful multiple sequence alignment browser."""

    homepage = "http://wasabiapp.org/software/prank/"
    url = "http://wasabiapp.org/download/prank/prank.source.170427.tgz"

    version("170427", sha256="623eb5e9b5cb0be1f49c3bf715e5fabceb1059b21168437264bdcd5c587a8859")

    depends_on("cxx", type="build")  # generated

    depends_on("mafft")
    depends_on("exonerate")
    depends_on("bpp-suite")  # for bppancestor
    conflicts("%gcc@7.2.0", when="@:150803")

    def install(self, spec, prefix):
        with working_dir("src"):
            filter_file("gcc", "{0}".format(spack_cc), "Makefile", string=True)
            filter_file("g++", "{0}".format(spack_cxx), "Makefile", string=True)
            if not spec.target.family == "x86_64":
                filter_file("-m64", "", "Makefile", string=True)
                filter_file("-pipe", "", "Makefile", string=True)

            make()
            mkdirp(prefix.bin)
            install("prank", prefix.bin)
