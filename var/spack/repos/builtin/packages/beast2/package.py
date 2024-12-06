# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Beast2(Package):
    """BEAST is a cross-platform program for Bayesian inference using MCMC
    of molecular sequences. It is entirely orientated towards rooted,
    time-measured phylogenies inferred using strict or relaxed molecular
    clock models. It can be used as a method of reconstructing phylogenies
    but is also a framework for testing evolutionary hypotheses without
    conditioning on a single tree topology."""

    homepage = "http://beast2.org/"
    url = "https://github.com/CompEvol/beast2/releases/download/v2.6.4/BEAST.v2.6.4.Linux.tgz"

    maintainers("snehring")

    license("LGPL-2.1-or-later")

    version(
        "2.7.4",
        sha256="f5086c74a0337190ae3459ef018468fc6b2eff68ae2b53fb5c96eb7b5df84004",
        url="https://github.com/CompEvol/beast2/releases/download/v2.7.4/BEAST.v2.7.4.Linux.x86.tgz",
    )
    version("2.6.7", sha256="05dcc619c2e10163f2c1089ec66149f6e53ec5a0583cd2cb8ffdccbbdb1d8183")
    version("2.6.4", sha256="4f80e2920eb9d87f3e9f64433119774dc67aca390fbd13dd480f852e3f8701a4")
    version("2.6.3", sha256="8899277b0d7124ab04dc512444d45f0f1a13505f3ce641e1f117098be3e2e20d")
    version("2.5.2", sha256="2feb2281b4f7cf8f7de1a62de50f52a8678ed0767fc72f2322e77dde9b8cd45f")
    version("2.4.6", sha256="84029c5680cc22f95bef644824130090f5f12d3d7f48d45cb4efc8e1d6b75e93")

    variant("beagle", default=True, description="Build with libbeagle support")

    depends_on("java")
    depends_on("java@17:", when="@2.7.0:")
    depends_on("javafx", when="@2.7.0:")
    depends_on("libbeagle", type="run", when="+beagle")

    def patch(self):
        # handle javafx stuff
        if self.spec.satisfies("@2.7.0:"):
            javafx = "--module-path {}".format(self.spec["javafx"].prefix.lib)
            modules = "--add-modules javafx.controls"
            with working_dir("bin"):
                for i in find(".", "*"):
                    filter_file(
                        r"(beast\.pkgmgmt.*\b)|(viz.*\b)", "{0} {1} \\1".format(javafx, modules), i
                    )

    def setup_run_environment(self, env):
        env.set("BEAST", self.prefix)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("examples", join_path(self.prefix, "examples"))
        install_tree("images", join_path(self.prefix, "images"))
        install_tree("lib", prefix.lib)
        if spec.satisfies("@:2.6.4"):
            template_dir = "templates"
        else:
            template_dir = "fxtemplates"
        install_tree(template_dir, join_path(self.prefix, template_dir))
