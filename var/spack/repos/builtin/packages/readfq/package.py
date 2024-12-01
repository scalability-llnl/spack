# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Readfq(Package):
    """Readfq is a collection of routines for parsing the FASTA/FASTQ format.
    It seamlessly parses both FASTA and multi-line FASTQ with a simple
    interface."""

    homepage = "https://github.com/lh3/readfq"
    git = "https://github.com/lh3/readfq.git"

    license("MIT")

    version("2013.04.10", commit="4fb766095d8f459e0f8025be70f9173673905d12")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
