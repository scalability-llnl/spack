# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prodigal(MakefilePackage):
    """Fast, reliable protein-coding gene prediction for prokaryotic
    genomes."""

    homepage = "https://github.com/hyattpd/Prodigal"
    url = "https://github.com/hyattpd/Prodigal/archive/v2.6.3.tar.gz"

    license("GPL-3.0-or-later")

    version("2.6.3", sha256="89094ad4bff5a8a8732d899f31cec350f5a4c27bcbdd12663f87c9d1f0ec599f")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("INSTALLDIR={0}".format(self.prefix), "install")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
