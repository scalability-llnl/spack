# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from os import symlink

from spack.package import *


class Smof(Package):
    """Explore and analyze biological sequence data"""

    homepage = "https://github.com/incertae-sedis/smof"
    url = "https://github.com/incertae-sedis/smof/archive/2.13.1.tar.gz"

    license("GPL-2.0-or-later")

    version("2.13.1", sha256="bae75703728c62398f2af58b142ab2555f9be2224e13ff108913607777ea2a2e")

    depends_on("python@3:", type="run")

    def install(self, spec, prefix):
        # install sources
        install_tree(".", prefix)

        # add command
        mkdirp(prefix.bin)

        symlink(join_path(prefix, "smof.py"), join_path(prefix.bin, "smof"))
