# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Microbiomeutil(MakefilePackage, SourceforgePackage):
    """Microbiome analysis utilities"""

    homepage = "https://microbiomeutil.sourceforge.net/"
    sourceforge_mirror_path = "microbiomeutil/microbiomeutil-r20110519.tgz"

    version("20110519", sha256="9233de80ea57bfb9e9371cbe7e3bfad2d4a51168fddaf60fa144c4046c80d823")

    depends_on("c", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on("blast-plus")
    depends_on("cdbfasta")

    def install(self, spec, prefix):
        install_tree("ChimeraSlayer", prefix.ChimeraSlayer)
        install_tree("NAST-iEr", join_path(prefix, "NAST-iEr"))
        install_tree("TreeChopper", prefix.TreeChopper)
        install_tree("WigeoN", prefix.WigeoN)
        install_tree("docs", prefix.docs)
        install_tree("RESOURCES", prefix.resources)
        install_tree("AmosCmp16Spipeline", prefix.AmosCmp16Spipeline)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.ChimeraSlayer)
        env.prepend_path("PATH", join_path(self.prefix, "NAST-iEr"))
        env.prepend_path("PATH", self.prefix.TreeChopper)
        env.prepend_path("PATH", self.prefix.WigeoN)
