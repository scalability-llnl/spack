# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Beast1(Package):
    """BEAST is a cross-platform program for Bayesian
    analysis of molecular sequences using MCMC."""

    homepage = "https://beast.community/"

    version("1.10.4", sha256="be652c4d55953f7c6c7a9d3eb3de203c77dc380e81ad81cfe0492408990c36a8")
    version("1.8.4", sha256="c14e93976008463108aefa34ecc23287ab70703caccf4962e36e295207120d78")

    depends_on("c", type="build")  # generated

    variant("beagle", default=True, description="Build with libbeagle support")

    depends_on("java", type="run")
    depends_on("libbeagle", type=("build", "link", "run"), when="+beagle")

    def url_for_version(self, ver):
        base = "https://github.com/beast-dev/beast-mcmc/releases/download"
        return "{0}/v{1}/BEASTv{1}.tgz".format(base, ver.dotted)

    def setup_run_environment(self, env):
        env.set("BEAST1", self.prefix)
        env.set("BEAST_LIB", self.prefix.lib)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("examples", prefix.examples)
        install_tree("images", prefix.images)
        install_tree("lib", prefix.lib)
        install_tree("doc", prefix.doc)
