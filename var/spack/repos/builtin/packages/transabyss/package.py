# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Transabyss(Package):
    """De novo assembly of RNAseq data using ABySS"""

    homepage = "https://www.bcgsc.ca/platform/bioinfo/software/trans-abyss"
    url = "https://www.bcgsc.ca/platform/bioinfo/software/trans-abyss/releases/1.5.5/transabyss-1.5.5.zip"

    version("1.5.5", sha256="7804961c13296c587a1b22180dd3f02091a4494cbbd04fc33c2060599caadb0b")

    depends_on("abyss@1.5.2")
    depends_on("python@2.7.6:", type=("build", "run"))
    depends_on("py-python-igraph@0.7.0:", type=("build", "run"))
    depends_on("blat")

    def install(self, spec, prefix):
        install("transabyss", prefix)
        install("transabyss-merge", prefix)
        install_tree("bin", prefix.bin)
        install_tree("utilities", prefix.utilities)
