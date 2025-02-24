# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRdpack(RPackage):
    """Update and Manipulate Rd Documentation Objects.

    Functions for manipulation of R documentation objects, including functions
    reprompt() and ereprompt() for updating 'Rd' documentation for functions,
    methods and classes; 'Rd' macros for citations and import of references
    from 'bibtex' files for use in 'Rd' files and 'roxygen2' comments; 'Rd'
    macros for evaluating and inserting snippets of 'R' code and the results of
    its evaluation or creating graphics on the fly; and many functions for
    manipulation of references and Rd files."""

    cran = "Rdpack"

    version("2.6.1", sha256="39626397c4ab1706bfdc53433dbaa0a6cb691dcba68173945b5a9eb041acf945")
    version("2.4", sha256="7652add12b30fcba1f3a12493a089a4166079e78c47b95802a98595a3ff53581")
    version("2.3", sha256="c45e1ab8352b92ce03f26ece1f4db3716959fca2af9e826d5bd3c76b2151f7c5")
    version("2.1.3", sha256="8381a8866b9acf5acb2c80069684339c3921f1b45fa202719e8f6852fb4d55b8")
    version("2.1", sha256="26e094fe3c077fb2a99e95c5bd94015a5f993a4a5f5d217829b4872ff004bfce")
    version("0.11-0", sha256="8fb449c80fbe931cdce51f728fb03a1978009ccce66fd6b9edacdc6ff4118d85")

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r-rbibutils@1.3:", type=("build", "run"), when="@2.1:")

    depends_on("r-bibtex@0.4.0:", type=("build", "run"), when="@:0.11-0")
    depends_on("r-gbrd", type=("build", "run"), when="@:2.1")
