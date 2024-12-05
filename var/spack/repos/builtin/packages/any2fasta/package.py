# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Any2fasta(Package):
    """any2fasta: Convert various sequence formats to FASTA"""

    homepage = "https://github.com/tseemann/any2fasta"
    url = "https://github.com/tseemann/any2fasta/archive/refs/tags/v0.4.2.tar.gz"

    license("GPL-3.0-only")

    version("0.4.2", sha256="e4cb2ddccda6298f5b0aee0c10184a75307a08b584d2abbfbf0d59d37b197e73")
    version("0.2.3", sha256="197cd1e18adebe28b71a1448c5107804b7093b2aa83c4bcfd8edd3fc4ed485df")
    version("0.1.2", sha256="ef035595756df7dca1f8a503ee26f8479393953bc67d8870c9965b6d5ade2674")

    depends_on("perl@5.10:", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("any2fasta", prefix.bin)
