# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diffsplice(MakefilePackage):
    """A novel tool for discovering and quantitating alternative splicing
    variants present in an RNA-seq dataset, without relying on annotated
    transcriptome or pre-determined splice pattern."""

    homepage = "http://www.netlab.uky.edu/p/bioinfo/DiffSplice"
    url = "https://protocols.netlab.uky.edu/~yin/download/diffsplice/diffsplice_0.1.1.tgz"

    license("GPL-3.0-only")

    version("0.1.2beta", sha256="cc06dcb9f8d98b2184f0dd5863b79bdd6a8cd33b9418e6549b7ea63e90ee1aa6")
    version("0.1.1", sha256="9740426692b0e5f92b943b127014c1d9815bed2938b5dd9e9d0c5b64abbb5da6")

    depends_on("cxx", type="build")  # generated

    def edit(self, spec, prefix):
        if spec.target.family == "aarch64":
            makefile = FileFilter(join_path(self.build_directory, "Makefile"))
            makefile.filter("-m64", "")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("diffsplice", prefix.bin)
