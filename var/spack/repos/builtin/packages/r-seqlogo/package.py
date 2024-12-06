# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSeqlogo(RPackage):
    """Sequence logos for DNA sequence alignments.

    seqLogo takes the position weight matrix of a DNA sequence motif and
    plots the corresponding sequence logo as introduced by Schneider and
    Stephens (1990)."""

    bioc = "seqLogo"

    version("1.66.0", commit="6214c1733fe25da86071afba4210068816e4d74f")
    version("1.64.0", commit="75ff6c0689fce541f054d33750acb6224d14ed4e")
    version("1.62.0", commit="f2d0b53b1411ea98299201a8125a85f4cbf7c9cd")
    version("1.60.0", commit="4115c8e1d01accb8c8cc1cf96f23359466827e16")
    version("1.56.0", commit="169260c43fc58dc75becb3b7842cac3d0038a8d5")
    version("1.50.0", commit="57986221c90c3920f9829756c4b3ee566dc1e14d")
    version("1.48.0", commit="dde85582e7fd0c08c5b8bc73f9aed8f23b727d9d")
    version("1.46.0", commit="e78be03db5f6a516138aeea6aa9512685633a4a2")
    version("1.44.0", commit="4cac14ff29f413d6de1a9944eb5d21bfe5045fac")
    version("1.42.0", commit="d7e04726c813282aa3f47a9ee98c5e1cec9bdddd")

    depends_on("r@4.2:", type=("build", "run"), when="@1.62.0:")
