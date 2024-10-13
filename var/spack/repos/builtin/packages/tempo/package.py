# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tempo(AutotoolsPackage):
    """Tempo is a program for pulsar timing data analysis."""

    homepage = "https://tempo.sourceforge.net/"
    git = "git://git.code.sf.net/p/tempo/tempo.git"

    version("develop")
    version("LWA-10-17-2020", commit="6bab1083350eca24745eafed79a55156bdd1e7d5")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def setup_dependent_run_environment(self, spack_env, dependent_spec):
        spack_env.set("TEMPO_DIR", self.prefix)
