# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Scallop(AutotoolsPackage):
    """Scallop is a reference-based transcriptome assembler for RNA-seq"""

    homepage = "https://github.com/Kingsford-Group/scallop"
    url = "https://github.com/Kingsford-Group/scallop/releases/download/v0.10.5/scallop-0.10.5.tar.gz"

    license("BSD-3-Clause")

    version("0.10.5", sha256="b09e3c61f1b3b1da2a96d9d8429d80326a3bb14f5fe6af9b5e87570d4b86937a")
    version("0.10.3", sha256="04eb3ab27ed8c7ae38e1780d6b2af16b6a2c01807ffafd59e819d33bfeff58a0")

    depends_on("cxx", type="build")  # generated

    depends_on("clp")
    depends_on("boost")
    depends_on("htslib@1.5:")

    def configure_args(self):
        return [
            "--with-clp={0}".format(self.spec["clp"].prefix),
            "--with-htslib={0}".format(self.spec["htslib"].prefix),
            "--with-boost={0}".format(self.spec["boost"].prefix),
        ]
