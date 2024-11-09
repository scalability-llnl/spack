# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trimal(MakefilePackage):
    """A tool for automated alignment trimming in large-scale
    phylogenetic analyses"""

    homepage = "https://github.com/scapella/trimal"
    url = "https://github.com/scapella/trimal/archive/v1.4.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.4.1", sha256="cb8110ca24433f85c33797b930fa10fe833fa677825103d6e7f81dd7551b9b4e")

    depends_on("cxx", type="build")  # generated

    build_directory = "source"

    def install(self, sinstall_treepec, prefix):
        mkdirp(prefix.bin)
        binaries = ["trimal", "readal", "statal"]
        with working_dir(self.build_directory):
            for b in binaries:
                install(b, prefix.bin)
