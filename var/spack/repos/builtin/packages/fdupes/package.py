# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fdupes(AutotoolsPackage):
    """FDUPES is a program for identifying or deleting duplicate files
    residing within specified directories."""

    homepage = "https://github.com/adrianlopezroche/fdupes"
    url      = "https://github.com/adrianlopezroche/fdupes/releases/download/v2.1.2/fdupes-2.1.2.tar.gz"

    maintainers = ['michaelkuhn']

    version('2.1.2', sha256='cd5cb53b6d898cf20f19b57b81114a5b263cc1149cd0da3104578b083b2837bd')

    variant('ncurses', default=True, description='ncurses support')

    depends_on('ncurses', when='+ncurses')

    def configure_args(self):
        return self.with_or_without('ncurses')
