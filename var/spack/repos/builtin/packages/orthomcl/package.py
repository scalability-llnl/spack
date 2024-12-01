# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Orthomcl(Package):
    """OrthoMCL is a genome-scale algorithm for grouping orthologous protein
    sequences."""

    homepage = "https://orthomcl.org/orthomcl/"
    url = "https://orthomcl.org/common/downloads/software/v2.0/orthomclSoftware-v2.0.9.tar.gz"

    version("2.0.9", sha256="5f96d23ff255778535c4926d75b19f059db0c01be1ac599289d2431115d68640")

    depends_on("perl", type=("build", "run"))
    depends_on("blast-plus")
    depends_on("mcl")
    depends_on("mariadb")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("config", prefix.config)
        install_tree("doc", prefix.doc)
        install_tree("lib", prefix.lib)

    def setup_run_environment(self, env):
        env.prepend_path("PERL5LIB", self.prefix.lib)
