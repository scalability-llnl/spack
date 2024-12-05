# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Barrnap(Package):
    """Barrnap predicts the location of ribosomal RNA genes in genomes."""

    homepage = "https://github.com/tseemann/barrnap"
    url = "https://github.com/tseemann/barrnap/archive/0.8.tar.gz"

    license("CC0-1.0")

    version("0.9", sha256="36c27cd4350531d98b3b2fb7d294a2d35c15b7365771476456d7873ba33cce15")
    version("0.8", sha256="82004930767e92b61539c0de27ff837b8b7af01236e565f1473c63668cf0370f")
    version("0.7", sha256="ef2173e250f06cca7569c03404c9d4ab6a908ef7643e28901fbe9a732d20c09b")
    version("0.6", sha256="272642a41634623bda34dccdce487ab791925fa769e3e575d53014956a1f9dce")

    depends_on("hmmer@3.1b:", type="run")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("db", prefix.db)
