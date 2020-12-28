# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTximport(RPackage):
    """Import and summarize transcript-level estimates for transcript- and
       gene-level analysis.

       Imports transcript-level abundance, estimated counts and transcript
       lengths, and summarizes into matrices for use with downstream gene-level
       analysis packages. Average transcript length, weighted by sample-
       specific transcript abundance estimates, is provided as a matrix which
       can be used as an offset for different expression of gene-level
       counts."""

    homepage = "https://bioconductor.org/packages/tximport"
    git      = "https://git.bioconductor.org/packages/tximport.git"

    version('1.12.3', commit='acbdead961471c3b910d720f73bd0af1b7a07c57')
    version('1.10.1', commit='cd8f81cf7140f61d4a4f25f89451fb49e2cd4bd3')
    version('1.8.0', commit='cc91b8389ca4c16b0f588bdeb63d051a11e8a705')
    version('1.6.0', commit='0b1ba6c6622e02b954812c88454c28e8efb75e0b')
    version('1.4.0', commit='bfbd2436eca21acf212b76a658b49cfb5e116d6b')
