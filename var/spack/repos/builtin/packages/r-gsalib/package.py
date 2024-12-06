# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsalib(RPackage):
    """Utility Functions For GATK.

    This package contains utility functions used by the Genome Analysis
    Toolkit (GATK) to load tables and plot data. The GATK is a toolkit for
    variant discovery in high-throughput sequencing data."""

    cran = "gsalib"

    license("MIT")

    version("2.2.1", sha256="3da3a4b959142a0d694a843e39143bfce82a6de197c6cc92650a28ac05f3bf90")
    version("2.1", sha256="e1b23b986c18b89a94c58d9db45e552d1bce484300461803740dacdf7c937fcc")
