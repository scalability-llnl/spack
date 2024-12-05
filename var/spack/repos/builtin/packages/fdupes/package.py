# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fdupes(AutotoolsPackage):
    """FDUPES is a program for identifying or deleting duplicate files
    residing within specified directories."""

    homepage = "https://github.com/adrianlopezroche/fdupes"
    url = "https://github.com/adrianlopezroche/fdupes/releases/download/v2.1.2/fdupes-2.1.2.tar.gz"

    maintainers("michaelkuhn")

    license("MIT")

    version("2.2.1", sha256="846bb79ca3f0157856aa93ed50b49217feb68e1b35226193b6bc578be0c5698d")
    version("2.1.2", sha256="cd5cb53b6d898cf20f19b57b81114a5b263cc1149cd0da3104578b083b2837bd")

    depends_on("c", type="build")  # generated

    variant("ncurses", default=True, description="ncurses support")

    depends_on("ncurses", when="+ncurses")
    depends_on("pcre2", when="+ncurses")

    def configure_args(self):
        return self.with_or_without("ncurses")
