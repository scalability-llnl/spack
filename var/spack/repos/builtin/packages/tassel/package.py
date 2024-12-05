# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tassel(Package):
    """TASSEL is a software package to evaluate traits associations,
    evolutionary patterns, and linkage disequilibrium."""

    homepage = "https://www.maizegenetics.net/tassel"
    git = "https://bitbucket.org/tasseladmin/tassel-5-standalone.git"
    maintainers("snehring")

    version("5.2.86", commit="6557864512a89932710b9f53c6005a35ad6c526e")
    version("5.2.39", commit="ae96ae75c3c9a9e8026140b6c775fa4685bdf531")
    version(
        "3.0.174",
        commit="612a92c0f677d6ec040c17e146671974a3cdc2da",
        git="git://git.code.sf.net/p/tassel/tassel3-standalone.git",
    )

    depends_on("java", type=("build", "run"))
    depends_on("perl", type=("build", "run"))

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)

    def setup_run_environment(self, env):
        env.prepend_path("CLASSPATH", self.prefix.bin.lib)
