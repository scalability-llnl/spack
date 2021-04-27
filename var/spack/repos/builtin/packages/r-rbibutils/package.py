# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRbibutils(RPackage):
    """Convert Between Bibliography Formats

    Converts between a number of bibliography formats, including 'BibTeX',
    'BibLaTeX' and 'Bibentry'. Includes a port of the 'bibutils' utilities by
    Chris Putnam <https://sourceforge.net/projects/bibutils/>. Supports all
    bibliography formats and character encodings implemented in 'bibutils'."""

    homepage = "https://geobosh.github.io/rbibutils/"
    url      = "https://cloud.r-project.org/src/contrib/rbibutils_2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rbibutils"

    version('2.0', sha256='03d13abee321decb88bc4e7c9f27276d62a4a880fa72bb6b86be91885010cfed')

    depends_on('r@2.10:', type=('build', 'run'))
