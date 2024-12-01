# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPfamDb(RPackage):
    """A set of protein ID mappings for PFAM.

    A set of protein ID mappings for PFAM assembled using data from
    public repositories."""

    bioc = "PFAM.db"
    url = "https://www.bioconductor.org/packages/release/data/annotation/src/contrib/PFAM.db_3.4.1.tar.gz"

    version(
        "3.17.0",
        url="https://bioconductor.org/packages/3.17/data/annotation/src/contrib/PFAM.db_3.17.0.tar.gz",
        sha256="8c4f8bebbf002df87ef7e4c4116be1676072e5c3ba0af1070d281a2ea6101712",
    )
    version(
        "3.16.0",
        url="https://bioconductor.org/packages/3.16/data/annotation/src/contrib/PFAM.db_3.16.0.tar.gz",
        sha256="8082aaa94eb962b2cf42cfaead8ff9e1bdbd12fdeae82a49d0f3b37bd50eb30c",
    )
    version(
        "3.15.0",
        url="https://bioconductor.org/packages/3.15/data/annotation/src/contrib/PFAM.db_3.15.0.tar.gz",
        sha256="e7036a5f76779ab6e8a32eb659c54f52426c4824dee02903cffd85bed372720f",
    )
    version(
        "3.14.0",
        url="https://bioconductor.org/packages/3.14/data/annotation/src/contrib/PFAM.db_3.14.0.tar.gz",
        sha256="25c1915079e8f93d04e2cc1ab791f7f47813aaab5ac394feaf57520bb292d616",
    )
    version(
        "3.12.0",
        url="https://bioconductor.org/packages/3.12/data/annotation/src/contrib/PFAM.db_3.12.0.tar.gz",
        sha256="ec42d067522baf2d7d3ca78d4f8cc0dac08a4b98f1d890f52424e5d5b16f2fe9",
    )
    version(
        "3.10.0",
        url="https://bioconductor.org/packages/3.10/data/annotation/src/contrib/PFAM.db_3.10.0.tar.gz",
        sha256="038888f95ce69230ac0e0b08aa3bcb09965682415520d437a7fb0a031eefe158",
    )
    version(
        "3.4.1",
        url="https://bioconductor.org/packages/3.5/data/annotation/src/contrib/PFAM.db_3.4.1.tar.gz",
        sha256="fc45a0d53139daf85873f67bd3f1b68f2d883617f4447caddbd2d7dcc58a393f",
    )

    depends_on("r@2.7.0:", when="@3.4.1:", type=("build", "run"))
    depends_on("r-annotationdbi@1.37.4:", type=("build", "run"), when="@3.4.1:")
    depends_on("r-annotationdbi@1.47.1:", type=("build", "run"), when="@3.10.0:")
    depends_on("r-annotationdbi@1.51.3:", type=("build", "run"), when="@3.12.0:")
    depends_on("r-annotationdbi@1.55.1:", type=("build", "run"), when="@3.14.0:")
    depends_on("r-annotationdbi@1.57.1:", type=("build", "run"), when="@3.15.0:")
    depends_on("r-annotationdbi@1.59.1:", type=("build", "run"), when="@3.16.0:")
    depends_on("r-annotationdbi@1.61.0:", type=("build", "run"), when="@3.17.0:")
