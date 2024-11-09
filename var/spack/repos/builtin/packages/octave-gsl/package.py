# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OctaveGsl(OctavePackage, SourceforgePackage):
    """Octave bindings to the GNU Scientific Library"""

    homepage = "https://octave.sourceforge.io/gsl/"
    sourceforge_mirror_path = "octave/gsl-2.1.1.tar.gz"

    license("GPL-2.0-or-later")

    version("2.1.1", sha256="d028c52579e251c3f21ebfdf065dffab3ad7893434efda33b501225ef1ea6ed3")

    depends_on("cxx", type="build")  # generated

    depends_on("gsl@2.4:")
    extends("octave@2.9.7:")

    def setup_build_environment(self, env):
        env.prepend_path("PKG_CONFIG_PATH", self.spec["gsl"].prefix)
