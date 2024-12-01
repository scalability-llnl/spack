# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rdptools(MakefilePackage):
    """Collection of commonly used RDP Tools for easy building."""

    homepage = "https://github.com/rdpstaff/RDPTools"
    url = "https://github.com/rdpstaff/RDPTools/archive/2.0.2.tar.gz"

    version("2.0.2", sha256="fc3d7f8129b45e602fc2c23e5e037a7f48c14d5a6b05c64f8c1d48e9767ac01d")

    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/rdptools/meta.yaml
    depends_on("java")
    depends_on("ant")
    depends_on("python")

    def install(self, spec, prefix):
        install_tree(".", prefix)
