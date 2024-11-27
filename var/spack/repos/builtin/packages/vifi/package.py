# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vifi(Package):
    """ViFi is a collection of python and perl scripts
    for identifying viral integration and fusion mRNA reads from NGS data."""

    homepage = "https://github.com/namphuon/ViFi"
    git = "https://github.com/namphuon/ViFi.git"

    license("GPL-3.0-only")

    version("master", branch="master")

    depends_on("perl", type="run")
    depends_on("python", type="run")
    depends_on("py-pysam", type="run")
    depends_on("hmmer", type="run")

    def install(self, spec, prefix):
        install_tree("scripts", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("test", prefix.test)
        install("LICENSE", prefix)
        install("README.md", prefix)
        install("TUTORIAL.md", prefix)
