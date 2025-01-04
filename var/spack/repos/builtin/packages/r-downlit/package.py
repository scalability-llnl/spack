# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDownlit(RPackage):
    """Syntax Highlighting and Automatic Linking.

    Syntax highlighting of R code, specifically designed for the needs of
    'RMarkdown' packages like 'pkgdown', 'hugodown', and 'bookdown'. It
    includes linking of function calls to their documentation on the web, and
    automatic translation of ANSI escapes in output to the equivalent HTML."""

    cran = "downlit"

    license("MIT")

    version("0.4.4", sha256="55c377dcee4adc48c1060e14079f3d1832453d066a2cf070530caa210c48f828")
    version("0.4.2", sha256="33dff66909104d1a5ba8e57b1288986e82b61fd5e91dce0cd358d53724b37e3c")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.4.4:")
    depends_on("r-brio", type=("build", "run"))
    depends_on("r-desc", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-evaluate", type=("build", "run"))
    depends_on("r-fansi", type=("build", "run"))
    depends_on("r-memoise", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-yaml", type=("build", "run"))
