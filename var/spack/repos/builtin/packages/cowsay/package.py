# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cowsay(Package):
    """A program that generates ASCII pictures of a cow with a message."""

    homepage = "https://github.com/tnalpgge/rank-amateur-cowsay"
    url = "https://github.com/tnalpgge/rank-amateur-cowsay/archive/cowsay-3.04.tar.gz"

    license("Artistic-1.0-Perl OR GPL-2.0-or-later")

    version("3.04", sha256="d8b871332cfc1f0b6c16832ecca413ca0ac14d58626491a6733829e3d655878b")

    depends_on("perl", type=("run"))

    def install(self, spec, prefix):
        install_sh = Executable("./install.sh")
        install_sh(prefix)
