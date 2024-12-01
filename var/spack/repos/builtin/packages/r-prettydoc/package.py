# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPrettydoc(RPackage):
    """Creating Pretty Documents from R Markdown.

    Creating tiny yet beautiful documents and vignettes from R Markdown. The
    package provides the 'html_pretty' output format as an alternative to the
    'html_document' and 'html_vignette' engines that convert R Markdown into
    HTML pages. Various themes and syntax highlight styles are supported."""

    cran = "prettydoc"

    version("0.4.1", sha256="1094a69b026238d149435472b4f41c75151c7370a1be6c6332147c88ad4c4829")

    depends_on("r-rmarkdown@1.17:", type=("build", "run"))
    depends_on("pandoc@1.12.3:", type="build")
