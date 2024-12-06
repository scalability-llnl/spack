# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPiggyback(RPackage):
    """Managing Larger Data on a GitHub Repository

    Because larger (> 50 MB) data files cannot easily be committed to git, a
    different approach is required to manage data associated with an analysis in
    a GitHub repository. This package provides a simple work-around by allowing
    larger (up to 2 GB) data files to piggyback on a repository as assets
    attached to individual GitHub releases. These files are not handled by git
    in any way, but instead are uploaded, downloaded, or edited directly by
    calls through the GitHub API. These data files can be versioned manually by
    creating different releases. This approach works equally well with public or
    private repositories. Data can be uploaded and downloaded programmatically
    from scripts. No authentication is required to download data from public
    repositories."""

    homepage = "https://github.com/ropensci/piggyback"
    cran = "piggyback"

    maintainers("jgaeb")

    license("GPL-3.0-only")

    version("0.1.5", sha256="983b5a46792ff5f2895f36ee29afcbd7723d05fe3daefdaefaada12987e36aee")
    version("0.1.4", sha256="9e9d6d75e13f82559e5322182af557b3c79f9a6e9b0bc8c1e1b193544dcda511")
    version("0.1.3", sha256="6fccae21a97653f6a1d90d97c4f089bf403126a808f4b4023f4b0c6a496e0b07")
    version("0.1.2", sha256="39611437a136e98a89c157ec3aa9f5daf3c38e0b761c446d9eaf76c50ee6ef62")
    version("0.1.1", sha256="03d966bbcbac8dcda4afc1667faf95fe6aa0047e2cd0d063104d9c33274484b4")
    version("0.1.0", sha256="71c7484c879f9e9644f3d6d6fe021213a8995d998f6b90b7143093ed11f858a0")
    version("0.0.11", sha256="bac9b0cde1be9b01574a0dffa8ffd08457bdd4edb2bcb1d455ec9547ee9f959d")
    version("0.0.10", sha256="7f0134c234cf24ded142037f132349574851d22dc97f949784deed7a7897a721")
    version("0.0.9", sha256="05668540d457d5945512a802a364487d10671556d675f4c287f2b3afbc9156bf")
    version("0.0.8", sha256="2e38f51d0ab3f55c5ddb49002693164a5f4c630b2055b8ae36d94875b1f427b0")
    version("0.0.7", sha256="df0692deacca58b893360bdfb2e295ba8bc785bcb99f4a2cd8c6738ed0c4f865")

    depends_on("r-gh", type=("build", "run"), when="@0.0.7:")
    depends_on("r-httr", type=("build", "run"), when="@0.0.7:")
    depends_on("r-jsonlite", type=("build", "run"), when="@0.0.7:")
    depends_on("r-git2r", type=("build", "run"), when="@0.0.7:0.0.11")
    depends_on("r-fs", type=("build", "run"), when="@0.0.7:")
    depends_on("r-usethis", type=("build", "run"), when="@0.0.7:0.0.11")
    depends_on("r-crayon", type=("build", "run"), when="@0.0.7:0.1.1")
    depends_on("r-clisymbols", type=("build", "run"), when="@0.0.7:0.1.1")
    depends_on("r-magrittr", type=("build", "run"), when="@0.0.7:0.1.0")
    depends_on("r-lubridate", type=("build", "run"), when="@0.0.7:")
    depends_on("r-memoise", type=("build", "run"), when="@0.0.7:")
    depends_on("r-cli", type=("build", "run"), when="@0.1.2:")
    depends_on("r-glue", type=("build", "run"), when="@0.1.2:")
