# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fimpute(Package):
    """FImpute uses an overlapping sliding window approach to efficiently
    exploit relationships or haplotype similarities between target and
    reference individuals."""

    homepage = "http://www.aps.uoguelph.ca/~msargol/fimpute/"
    url = "http://www.aps.uoguelph.ca/~msargol/fimpute/FImpute_Linux.zip"

    version("2014-01", sha256="aecda2dfdd4e3ef6f2331cc1d479e6f297f722fcdca455ca05bb047405534461")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("FImpute", prefix.bin)
