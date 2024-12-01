# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snptest(Package):
    """SNPTEST is a program for the analysis of single SNP association in
    genome-wide studies."""

    homepage = "https://mathgen.stats.ox.ac.uk/genetics_software/snptest/snptest.html"
    url = "https://www.well.ox.ac.uk/~gav/resources/snptest_v2.5.2_linux_x86_64_dynamic.tgz"

    version("2.5.6", sha256="22582e49f4a16edf52fe44e8f5e6f3479871658ec1be6341275f6f15d9cbd301")
    version("2.5.2", sha256="1ffa3ebafa2c5db4866a38e01bb09f43df7973d053423ce67221cb3f8acb30f6")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(f"snptest_v{self.version}", prefix.bin)
