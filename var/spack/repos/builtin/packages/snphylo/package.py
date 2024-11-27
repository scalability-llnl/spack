# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snphylo(Package):
    """A pipeline to generate a phylogenetic tree from huge SNP data"""

    homepage = "http://chibba.pgml.uga.edu/snphylo/"
    url = "https://github.com/thlee/SNPhylo/archive/refs/tags/20180901.tar.gz"

    license("GPL-2.0-only")

    version("20180901", sha256="46273bcafc8f6cc2465fc524926af7dd122bcc7b7ce1b7c3f5c278111c3a9ddd")
    version(
        "2016-02-04",
        sha256="d9e144021c83dbef97bebf743b92109ad0afcfe70f37c244059b43f11b8a50da",
        deprecated=True,
    )

    depends_on("python", type=("build", "run"))
    depends_on("r", type=("build", "run"))
    depends_on("r-phangorn", type=("build", "run"))
    depends_on("r-gdsfmt", type=("build", "run"))
    depends_on("r-snprelate", type=("build", "run"))
    depends_on("r-getopt", type=("build", "run"))
    depends_on("muscle")
    depends_on("phylip")

    def install(self, spec, prefix):
        install_answer = ["y", "y", "y", "y"]
        install_answer_input = "spack-config.in"
        with open(install_answer_input, "w") as f:
            f.writelines(install_answer)
        with open(install_answer_input, "r") as f:
            bash = which("bash")
            bash("./setup.sh", input=f)
            install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec.prefix)
