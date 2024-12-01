# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Rnaquast(Package):
    """Quality assessment of de novo transcriptome assemblies from RNA-Seq data

    rnaQUAST is a tool for evaluating RNA-Seq assemblies using reference genome
    and gene database. In addition, rnaQUAST is also capable of estimating gene
    database coverage by raw reads and de novo quality assessment
    using third-party software."""

    homepage = "https://github.com/ablab/rnaquast"
    url = "https://github.com/ablab/rnaquast/archive/refs/tags/v2.2.0.tar.gz"

    maintainers("dorton21")

    version("2.2.0", sha256="117dff9d9c382ba74b7b0ff24bc7b95b9ca6aa701ebf8afd22943aa54e382334")

    depends_on("python@2.5:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-gffutils", type=("build", "run"))
    depends_on("gmap-gsnap", type=("build", "run"))
    depends_on("blast-plus", type=("build", "run"))

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
        os.rename("%s/rnaQUAST.py" % prefix.bin, "%s/rnaQUAST" % prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", prefix.bin)
