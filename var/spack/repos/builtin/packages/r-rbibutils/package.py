# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRbibutils(RPackage):
    """Convert Between Bibliography Formats.

    Converts between a number of bibliography formats, including 'BibTeX',
    'BibLaTeX' and 'Bibentry'. Includes a port of the 'bibutils' utilities by
    Chris Putnam <https://sourceforge.net/projects/bibutils/>. Supports all
    bibliography formats and character encodings implemented in 'bibutils'."""

    cran = "rbibutils"

    license("GPL-2.0-only")

    version("2.2.16", sha256="9c7c0fba47f63b1749005311c7174b40e72d95c863a67b736a84b8ff375a2aaf")
    version("2.2.13", sha256="ac235c60bf191ad1830b93045af1b2fe50a6978f6f63cecc4c514a8ba339efc2")
    version("2.2.9", sha256="b22c07ff916ec338e5a8c6e7e4302f06c9b88d64ee6a59ee4bf5d83a3d5eff86")
    version("2.2.8", sha256="f1aecdeeba99042d34de19234238c5bbdc18a26f271f6adf9c9b7e349d50d152")
    version("2.2.7", sha256="7c9e6719556b8caa9fb58743b717e89f45e8e7018371bf16f07dc3c1f96a55c5")
    version("2.0", sha256="03d13abee321decb88bc4e7c9f27276d62a4a880fa72bb6b86be91885010cfed")

    depends_on("r@2.10:", type=("build", "run"))
