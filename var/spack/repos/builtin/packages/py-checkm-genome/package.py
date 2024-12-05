# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCheckmGenome(PythonPackage):
    """Assess the quality of microbial genomes recovered from isolates, single
    cells, and metagenomes"""

    homepage = "https://ecogenomics.github.io/CheckM"
    pypi = "checkm-genome/checkm-genome-1.0.11.tar.gz"

    license("GPL-3.0-or-later")

    version("1.2.1", sha256="33907aa7bbf029f8345e33df80d5c89b7a719041f55ece4f7470cd061c8eff76")

    # pip silently replaces distutils with setuptools
    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("hmmer@3.1b1:", type=("build", "run"))
    depends_on("pplacer", type=("build", "run"))
    depends_on("prodigal@2.6.1:", type=("build", "run"))
    depends_on("py-numpy@1.21.3:", type=("build", "run"))
    depends_on("py-scipy@1.7.3:", type=("build", "run"))
    depends_on("py-matplotlib@3.5.1:", type=("build", "run"))
    depends_on("py-pysam@0.19.0:", type=("build", "run"))
    depends_on("py-dendropy@4.5.2:", type=("build", "run"))
