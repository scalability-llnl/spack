# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minced(Package):
    """MinCED is a program to find Clustered Regularly Interspaced Short
    Palindromic Repeats (CRISPRs) in full genomes or environmental datasets
    such as metagenomes, in which sequence size can be anywhere from 100 to
    800 bp."""

    homepage = "https://github.com/ctSkennerton/minced"
    url = "https://github.com/ctSkennerton/minced/archive/0.2.0.tar.gz"

    license("GPL-3.0-only")

    version("0.4.2", sha256="35b6ee22fe6bdc26a31d0203a7dcc6bd1a19fd6733c60d80ceb44431884af165")
    version("0.3.2", sha256="334aee43292d0b657c4849f818ddfb3ac7811eb505502bf24a01d66719084b44")
    version("0.2.0", sha256="e1ca61e0307e6a2a2480bc0a1291a2c677110f34c3247d4773fdba7e95a6b573")
    version("0.1.6", sha256="035e343591b4595c571e17b0b3f526a01a23c3a47ebafb66f20ba667b29b3ed7")

    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install("minced", prefix.bin)
        install("minced.jar", prefix.bin)
