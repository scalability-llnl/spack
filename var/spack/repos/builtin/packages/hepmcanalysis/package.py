# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hepmcanalysis(MakefilePackage):
    """The HepMCAnalysis Tool is a tool for generator
    validation and comparisons."""

    homepage = "https://hepmcanalysistool.desy.de/"
    url = "https://hepmcanalysistool.desy.de/releases/HepMCAnalysis-00-03-04-13.tar.gz"

    version("3.4.13", sha256="be9937c6de493a5671258919493b0caa0cecca77853a2075f5cecce1071e0029")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    tags = ["hep"]

    depends_on("hepmc")
    depends_on("fastjet")
    depends_on("root")
    depends_on("clhep")

    patch("lcg.patch")

    def patch(self):
        filter_file(r"TDirectory::CurrentDirectory\(\)", r"gDirectory", "src/baseAnalysis.cc")
        filter_file(
            r"CXXFLAGS(.*)",
            r"CXXFLAGS\1 -std=c++" + self.spec["root"].variants["cxxstd"].value,
            "config.mk",
        )

    def setup_build_environment(self, env):
        env.set("HepMCdir", self.spec["hepmc"].prefix)
        env.set("FastJetdir", self.spec["fastjet"].prefix)
        env.set("CLHEPdir", self.spec["clhep"].prefix)

    def url_for_version(self, version):
        parts = [int(x) for x in str(version).split(".")]
        root = "https://hepmcanalysistool.desy.de/releases/HepMCAnalysis-00-"
        return root + "{0:02d}-{1:02d}-{2:02d}.tar.gz".format(*parts)

    def install(self, spec, prefix):
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
