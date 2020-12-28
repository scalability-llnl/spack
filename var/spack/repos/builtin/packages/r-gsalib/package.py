# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsalib(RPackage):
    """This package contains utility functions used by the Genome Analysis
    Toolkit (GATK) to load tables and plot data. The GATK is a toolkit for
    variant discovery in high-throughput sequencing data."""

    homepage = "https://cloud.r-project.org/package=gsalib"
    url      = "https://cloud.r-project.org/src/contrib/gsalib_2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gsalib"

    version('2.1', sha256='e1b23b986c18b89a94c58d9db45e552d1bce484300461803740dacdf7c937fcc')
