# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Atop(Package):
    """Atop is an ASCII full-screen performance monitor for Linux"""

    homepage = "https://www.atoptool.nl/index.php"
    url = "https://www.atoptool.nl/download/atop-2.2-3.tar.gz"

    license("GPL-2.0-or-later")

    version("2.5.0", sha256="4b911057ce50463b6e8b3016c5963d48535c0cddeebc6eda817e292b22f93f33")
    version("2.4.0", sha256="be1c010a77086b7d98376fce96514afcd73c3f20a8d1fe01520899ff69a73d69")
    version("2.3.0", sha256="73e4725de0bafac8c63b032e8479e2305e3962afbe977ec1abd45f9e104eb264")
    version("2.2.6", sha256="d0386840ee4df36e5d0ad55f144661b434d9ad35d94deadc0405b514485db615")
    version("2.2-3", sha256="c785b8a2355be28b3de6b58a8ea4c4fcab8fadeaa57a99afeb03c66fac8e055d")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("ncurses")

    def setup_build_environment(self, env):
        env.append_flags("LDFLAGS", "-ltinfo")

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        install("atop", join_path(prefix.bin, "atop"))
        mkdirp(join_path(prefix.man, "man1"))
        install(join_path("man", "atop.1"), join_path(prefix.man, "man1", "atop.1"))
