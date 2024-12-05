# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTxdbHsapiensUcscHg18Knowngene(RPackage):
    """Annotation package for TxDb object(s).

    Exposes an annotation databases generated from UCSC by exposing these as
    TxDb objects"""

    # This is a bioconductor package but ther is no available git repo
    bioc = "TxDb.Hsapiens.UCSC.hg18.knownGene"
    url = "https://bioconductor.org/packages/release/data/annotation/src/contrib/TxDb.Hsapiens.UCSC.hg18.knownGene_3.2.2.tar.gz"

    version("3.2.2", sha256="bc9ca40b4eab87f5ca64a4b876d42502b9b8e9f5983d745bfe0ee349d97b69fa")

    depends_on("r-genomicfeatures@1.21.30:", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
