# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoDb(RPackage):
    """A set of annotation maps describing the entire Gene Ontology.

    A set of annotation maps describing the entire Gene
    Ontology assembled using data from GO."""

    bioc = "GO.db"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/GO.db_3.4.1.tar.gz"

    version(
        "3.17.0",
        url="https://bioconductor.org/packages/3.17/data/annotation/src/contrib/GO.db_3.17.0.tar.gz",
        sha256="5dbe48060813c8c39a725b34d9c793ca76ef8e568fdc49f96f4a4bd8ba30401c",
    )
    version(
        "3.16.0",
        url="https://bioconductor.org/packages/3.16/data/annotation/src/contrib/GO.db_3.16.0.tar.gz",
        sha256="4652812d8ba380aeeb9b136efbc9365156397eec99c5ca36cfb8294139493b8e",
    )
    version(
        "3.15.0",
        url="https://bioconductor.org/packages/3.15/data/annotation/src/contrib/GO.db_3.15.0.tar.gz",
        sha256="bac91d73c57f206fa5bc4a501a2aaf61b365cf411181ce44353370cdbc132d99",
    )
    version(
        "3.14.0",
        url="https://bioconductor.org/packages/3.14/data/annotation/src/contrib/GO.db_3.14.0.tar.gz",
        sha256="45d0a681a662667d45b2472d160b72f7058ad0a28dd0ca24742e11ddfd87d8e7",
    )
    version(
        "3.12.1",
        url="https://bioconductor.org/packages/3.12/data/annotation/src/contrib/GO.db_3.12.1.tar.gz",
        sha256="e0316959d3d32096f9432c897413dff74fce53e15ead7917a7724467d971dab9",
    )
    version(
        "3.4.1",
        url="https://bioconductor.org/packages/3.5/data/annotation/src/contrib/GO.db_3.4.1.tar.gz",
        sha256="2fc2048e9d26edb98e35e4adc4d18c6df54f44836b5cc4a482d36ed99e058cc1",
    )

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r-annotationdbi@1.37.4:", type=("build", "run"))
    depends_on("r-annotationdbi@1.51.3:", type=("build", "run"), when="@3.12.1:")
    depends_on("r-annotationdbi@1.55.1:", type=("build", "run"), when="@3.14.0:")
    depends_on("r-annotationdbi@1.57.1:", type=("build", "run"), when="@3.15.0:")
    depends_on("r-annotationdbi@1.59.1:", type=("build", "run"), when="@3.16.0:")
    depends_on("r-annotationdbi@1.61.0:", type=("build", "run"), when="@3.17.0:")
