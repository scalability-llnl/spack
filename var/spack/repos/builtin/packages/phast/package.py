# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Phast(MakefilePackage):
    """PHAST is a freely available software package for comparative and
    evolutionary genomics."""

    homepage = "http://compgen.cshl.edu/phast/index.php"
    url = "https://github.com/CshlSiepelLab/phast/archive/v1.4.tar.gz"

    license("BSD-3-Clause")

    version("1.6", sha256="8100f6582008c5de46d2de05cee038f0f1ca3a50147031da1bc5e8744883cbe4")
    version("1.4", sha256="287c77599c51256a3adbd62ed217cb6d6a547fcec2c29262e9d61fa32ed92b99")

    depends_on("c", type="build")  # generated

    # phast cannot build with clapack using external blas
    depends_on("clapack~external-blas")

    build_directory = "src"

    @property
    def build_targets(self):
        targets = ["CLAPACKPATH={0}".format(self.spec["clapack"].prefix)]
        return targets

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file(
                r"\$\{PWD\}", "$(dir $(realpath $(firstword $(MAKEFILE_LIST))))", "make-include.mk"
            )
            filter_file(
                r"\$\{PWD\}", "$(dir $(realpath $(firstword $(MAKEFILE_LIST))))", "Makefile"
            )

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
