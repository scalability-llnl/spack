# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTximportdata(RPackage):
    """Import and summarize transcript-level estimates for transcript- and
    gene-level analysis.

    Imports transcript-level abundance, estimated counts and transcript
    lengths, and summarizes into matrices for use with downstream gene-level
    analysis packages. Average transcript length, weighted by sample-specific
    transcript abundance estimates, is provided as a matrix which can be used
    as an offset for different expression of gene-level counts."""

    bioc = "tximportData"

    version("1.28.0", commit="7de494ba12168e2766baffdd177d9cecc0642820")
    version("1.26.0", commit="8f6ef3e3ae54e6eb99fe915364f5174c4f50a986")
    version("1.24.0", commit="646f366fb25be359c95dc97c9369961c8d5ed942")
    version("1.22.0", commit="c576b18e43985baf8beab327cbc54afe8324659c")
    version("1.18.0", commit="24945f8dd1e4e441ad5145fb7a37a1630912f929")
