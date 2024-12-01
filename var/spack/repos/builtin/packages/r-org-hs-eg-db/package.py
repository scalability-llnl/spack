# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROrgHsEgDb(RPackage):
    """Genome wide annotation for Human.

    Genome wide annotation for Human, primarily based on mapping using Entrez
    Gene identifiers."""

    bioc = "org.Hs.eg.db"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz"

    version(
        "3.17.0",
        url="https://www.bioconductor.org/packages/3.17/data/annotation/src/contrib/org.Hs.eg.db_3.17.0.tar.gz",
        sha256="94714ea22b50d20523becbb665d9b27f2f147d3b1f77bc24ddcd3a245e201a0e",
    )
    version(
        "3.16.0",
        url="https://www.bioconductor.org/packages/3.16/data/annotation/src/contrib/org.Hs.eg.db_3.16.0.tar.gz",
        sha256="2d2e6fdefa0dbb61c86d4736e5a0d430745ae733e310f240b97b2cb3703a2c0a",
    )
    version(
        "3.15.0",
        url="https://www.bioconductor.org/packages/3.15/data/annotation/src/contrib/org.Hs.eg.db_3.15.0.tar.gz",
        sha256="1dc9bb6019e0f0a222b9ec84a1c5870cdbca480f45d9ad08e35f77278baa3c5f",
    )
    version(
        "3.14.0",
        url="https://www.bioconductor.org/packages/3.14/data/annotation/src/contrib/org.Hs.eg.db_3.14.0.tar.gz",
        sha256="0f87b3f1925a1d7007e5ad9200bdf511788bd1d7cb76f1121feeb109889c2b00",
    )
    version(
        "3.12.0",
        url="https://www.bioconductor.org/packages/3.12/data/annotation/src/contrib/org.Hs.eg.db_3.12.0.tar.gz",
        sha256="48a1ab5347ec7a8602c555d9aba233102b61ffa2765826e5c8890ff0003249bb",
    )
    version(
        "3.8.2",
        url="https://www.bioconductor.org/packages/3.9/data/annotation/src/contrib/org.Hs.eg.db_3.8.2.tar.gz",
        sha256="a0a16b7428f9e3d6ba54ebf4e05cd97a7bd298510ec4cf46ed2bed3e8f80db02",
    )
    version(
        "3.4.1",
        url="https://www.bioconductor.org/packages/3.5/data/annotation/src/contrib/org.Hs.eg.db_3.4.1.tar.gz",
        sha256="0f87b3f1925a1d7007e5ad9200bdf511788bd1d7cb76f1121feeb109889c2b00",
    )

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r-annotationdbi@1.37.4:", type=("build", "run"))
    depends_on("r-annotationdbi@1.43.1:", type=("build", "run"), when="@3.8.2:")
    depends_on("r-annotationdbi@1.51.3:", type=("build", "run"), when="@3.12.0:")
    depends_on("r-annotationdbi@1.55.1:", type=("build", "run"), when="@3.14.0:")
    depends_on("r-annotationdbi@1.57.1:", type=("build", "run"), when="@3.15.0:")
    depends_on("r-annotationdbi@1.59.1:", type=("build", "run"), when="@3.16.0:")
    depends_on("r-annotationdbi@1.61.0:", type=("build", "run"), when="@3.17.0:")
