# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Transrate(Package):
    """Transrate is software for de-novo transcriptome assembly quality
    analysis."""

    homepage = "https://hibberdlab.com/transrate/"

    if sys.platform == "darwin":
        version(
            "1.0.3",
            sha256="039eba81747dd53f65a99a61923369aae4ba341891215d31a2babe574ac99ca8",
            url="https://bintray.com/artifact/download/blahah/generic/transrate-1.0.3-osx.tar.gz",
        )
    else:
        version(
            "1.0.3",
            sha256="68d034ecd7012f1d3d505a2edd820c1155cd8b64d2acbf2ac833f30d3800141b",
            url="https://bintray.com/artifact/download/blahah/generic/transrate-1.0.3-linux-x86_64.tar.gz",
        )

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
