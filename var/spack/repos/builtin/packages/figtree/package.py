# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Figtree(Package):
    """FigTree is designed as a graphical viewer of phylogenetic trees and
    as a program for producing publication-ready figures. As with most of
    my programs, it was written for my own needs so may not be as polished
    and feature-complete as a commercial program. In particular it is
    designed to display summarized and annotated trees produced by BEAST."""

    homepage = "https://github.com/rambaut/figtree"
    url = "https://github.com/rambaut/figtree/releases/download/v1.4.3/FigTree_v1.4.3.tgz"

    version("1.4.4", sha256="529b867657b29e369cf81cd361e6a76bd713d488a63b91932df2385800423aa8")
    version("1.4.3", sha256="f497d4dd3a6d220f6b62495b6f47a12ade50d87dbd8d6089f168e94d202f937b")

    depends_on("java", type="run")

    def patch(self):
        # we have to change up the executable to point to the right program
        filter_file(
            "lib/figtree.jar",
            join_path(self.spec.prefix.lib, "figtree.jar"),
            "bin/figtree",
            string=True,
        )

        # also set proper executable flags
        os.chmod("bin/figtree", 0o775)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("bin", prefix.bin)

        mkdirp(prefix.lib)
        install_tree("lib", prefix.lib)
