# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class KaksCalculator(MakefilePackage, SourceforgePackage):
    """KaKs_Calculator adopts model selection and model averaging to calculate
    nonsynonymous (Ka) and synonymous (Ks) substitution rates, attempting to
    include as many features as needed for accurately capturing evolutionary
    information in protein-coding sequences."""

    homepage = "https://sourceforge.net/projects/kakscalculator2/"
    sourceforge_mirror_path = "kakscalculator2/KaKs_Calculator2.0.tar.gz"

    version("2.0", sha256="e2df719a2fecc549d8ddc4e6d8f5cfa4b248282dca319c1928eaf886d68ec3c5")

    depends_on("cxx", type="build")  # generated

    build_directory = "src"

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/kakscalculator2/KaKs_Calculator{0}.tar.gz"
        return url.format(version)

    # include<string.h> needs added to header file for compilation to work
    def patch(self):
        with working_dir(self.build_directory):
            header = FileFilter("base.h")
            header.filter("#include<time.h>", "#include<time.h>\n#include<string.h>")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("KaKs_Calculator", prefix.bin)
            install("ConPairs", prefix.bin)
            install("AXTConvertor", prefix.bin)
        install_tree("doc", prefix.doc)
        install_tree("examples", prefix.examples)
