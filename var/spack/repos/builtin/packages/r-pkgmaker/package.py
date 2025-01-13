# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgmaker(RPackage):
    """Development Utilities for R Packages.

    This package provides some low-level utilities to use for package
    development. It currently provides managers for multiple package specific
    options and registries, vignette, unit test and bibtex related utilities.
    It serves as a base package for packages like NMF, RcppOctave, doRNG, and
    as an incubator package for other general purposes utilities, that will
    eventually be packaged separately. It is still under heavy development and
    changes in the interface(s) are more than likely to happen."""

    cran = "pkgmaker"

    license("GPL-2.0-or-later")

    version("0.32.10", sha256="972b0473a64408ccc4841fa3f09a567cc32811e69c3c7e42a2f391a5eb2e2933")
    version("0.32.8", sha256="0ff3578d2c051b544c3f105cfe4801575aac1564add048f9e952c53a8ccd1745")
    version("0.32.2", sha256="ce45b22def771a9c90a414093823e6befe7e23489c500eeccee5154b44d3ef91")
    version("0.27", sha256="17a289d8f596ba5637b07077b3bff22411a2c2263c0b7de59fe848666555ec6a")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-registry", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-assertthat", type=("build", "run"), when="@0.32.2:")

    depends_on("r-stringi", type=("build", "run"), when="@:0.27")
    depends_on("r-magrittr", type=("build", "run"), when="@:0.27")
    depends_on("r-bibtex@0.4:", type=("build", "run"), when="@:0.27")
