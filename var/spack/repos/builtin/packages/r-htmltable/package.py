# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHtmltable(RPackage):
    """Tables with state-of-the-art layout elements such as row
    spanners, column spanners, table spanners, zebra striping, and
    more. While allowing advanced layout, the underlying css-structure
    is simple in order to maximize compatibility with word processors
    such as 'MS Word' or 'LibreOffice'. The package also contains a
    few text formatting functions that help outputting text
    compatible with HTML/'LaTeX'."""

    homepage = "https://cloud.r-project.org/package=htmlTable"
    url      = "https://cloud.r-project.org/src/contrib/htmlTable_1.11.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/htmlTable"

    version('1.13.1', sha256='689f32b65da6a57ad500e8d9ef3309d346401dca277c6b264a46c8d7c75884d0')
    version('1.11.2', sha256='64a273b1cdf07a7c57b9031315ca665f95d78e70b4320d020f64a139278877d1')
    version('1.9', sha256='5b487a7f33af77db7d987bf61f3ef2ba18bb629fe7b9802409f8b3485c603132')

    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-knitr@1.6:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-checkmate', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'), when="@1.11.0:")
    depends_on('r-rstudioapi@0.6:', type=('build', 'run'), when="@1.11.0:")
