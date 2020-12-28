# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBsgenomeHsapiensUcscHg19(RPackage):
    """Full genome sequences for Homo sapiens (Human) as provided by UCSC
    (hg19, Feb. 2009) and stored in Biostrings objects."""

    # This is a bioconductor package but there is no available git repo.
    homepage = "http://www.bioconductor.org/packages/release/data/annotation/html/BSgenome.Hsapiens.UCSC.hg19.html"
    url      = "http://www.bioconductor.org/packages/release/data/annotation/src/contrib/BSgenome.Hsapiens.UCSC.hg19_1.4.0.tar.gz"

    version('1.4.0', sha256='88f515e5c27dd11d10654250e3a0a9389e4dfeb0b1c2d43419aa7086e6c516f8')

    depends_on('r-bsgenome@1.33.5:', type=('build', 'run'))
