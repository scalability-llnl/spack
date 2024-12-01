# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Global(Package):
    """The Gnu Global tagging system"""

    homepage = "https://www.gnu.org/software/global"
    url = "http://tamacom.com/global/global-6.5.tar.gz"

    maintainers("gaber")

    license("LGPL-3.0-only")

    version("6.6.7", sha256="69a0f77f53827c5568176c1d382166df361e74263a047f0b3058aa2f2ad58a3c")
    version("6.6.6", sha256="758078afff98d4c051c58785c7ada3ed1977fabb77f8897ff657b71cc62d4d5d")
    version("6.6.4", sha256="987e8cb956c53f8ebe4453b778a8fde2037b982613aba7f3e8e74bcd05312594")
    version("6.5", sha256="4afd12db1aa600277b39113cc2d61dc59bd6c6b4ee8033da8bb6dd0c39a4c6a9")

    depends_on("exuberant-ctags", type=("build", "run"))
    depends_on("ncurses")

    patch("global-ncurse.patch")

    def install(self, spec, prefix):
        config_args = [
            "--prefix={0}".format(prefix),
            "--with-exuberant-ctags={0}".format(
                os.path.join(spec["exuberant-ctags"].prefix.bin, "ctags")
            ),
            "--with-ncurses={0}".format(spec["ncurses"].prefix),
        ]

        configure(*config_args)

        make()
        make("install")
