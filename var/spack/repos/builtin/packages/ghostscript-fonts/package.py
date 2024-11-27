# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class GhostscriptFonts(Package, SourceforgePackage):
    """Ghostscript Fonts"""

    homepage = "https://ghostscript.com/"
    sourceforge_mirror_path = (
        "gs-fonts/gs-fonts/8.11%20%28base%2035%2C%20GPL%29/" "ghostscript-fonts-std-8.11.tar.gz"
    )

    license("GPL-2.0-or-later")

    version("8.11", sha256="0eb6f356119f2e49b2563210852e17f57f9dcc5755f350a69a46a0d641a0c401")

    def install(self, spec, prefix):
        fdir = join_path(prefix.share, "font")
        mkdirp(fdir)
        files = glob.glob("*")
        for f in files:
            if not f.startswith("spack-build"):
                install(f, fdir)
