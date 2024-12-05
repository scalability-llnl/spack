# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Paml(MakefilePackage):
    """PAML is a package of programs for phylogenetic analyses of DNA or
    protein sewuences using maximum likelihood."""

    homepage = "http://abacus.gene.ucl.ac.uk/software/paml.html"
    url = "https://github.com/abacus-gene/paml/archive/refs/tags/4.10.7.tar.gz"
    git = "https://github.com/abacus-gene/paml.git"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("4.10.7", sha256="0f29e768b3797b69eadc6332c3d046d8727702052d56c3b729883626c0a5a4e3")
    version(
        "4.10.3",
        sha256="9b2a6e187e3f9f3bc55cd82db15eb701d43f031167d283a7c1b11c882b5d8a42",
        url="https://github.com/abacus-gene/paml/archive/refs/tags/untagged-a5659203e8ec0ddb58b8.tar.gz",
    )
    version(
        "4.10.0",
        sha256="6ef6a116f254185eb1cf7a2b975946fc9179a4b7dcb60a82f8fa8bbe6931897c",
        url="https://github.com/abacus-gene/paml/archive/refs/tags/v4.10.0.tar.gz",
    )
    version(
        "4.9h",
        sha256="623bf6cf4a018a4e7b4dbba189c41d6c0c25fdca3a0ae24703b82965c772edb3",
        url="http://abacus.gene.ucl.ac.uk/software/SoftOld/paml4.9h.tgz",
    )

    depends_on("c", type="build")  # generated

    build_directory = "src"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("baseml", prefix.bin)
            install("basemlg", prefix.bin)
            install("chi2", prefix.bin)
            install("codeml", prefix.bin)
            install("evolver", prefix.bin)
            install("infinitesites", prefix.bin)
            install("mcmctree", prefix.bin)
            install("pamp", prefix.bin)
            install("yn00", prefix.bin)
        install_tree("dat", prefix.dat)
        install_tree("Technical", prefix.Technical)
