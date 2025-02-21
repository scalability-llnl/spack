# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRoxygen2(RPackage):
    """In-Line Documentation for R.

    Generate your Rd documentation, 'NAMESPACE' file, and collation field using
    specially formatted comments. Writing documentation in-line with code makes
    it easier to keep your documentation up-to-date as your requirements
    change. 'Roxygen2' is inspired by the 'Doxygen' system for C++."""

    cran = "roxygen2"

    license("MIT")

    version("7.3.2", sha256="b788879f9132b7e2e656f442a6c592314676a9bf32d6a0a56e156cfa1ada011c")
    version("7.2.3", sha256="d844fab977d2575ab942fa1309ac7ff67f35f099a75d8b41c79efe6ea10416da")
    version("7.2.1", sha256="d2f0342591dc2b561fad8f6cf6fb3001e5e0bdd02be68bb2c6315f6bb82cda21")
    version("7.2.0", sha256="2ebfcfd567b9db6c606c6d42be1645b4e987f987995a2ad8954fa963a519448b")
    version("7.1.2", sha256="b3693d1eb57bb1c27134447ea7f64c353c085dd2237af7cfacc75fca3d2fc5fd")
    version("7.1.1", sha256="bdc55ded037d4366f4d25a0d69e880dacc0fa22bee20f595d45855eef8548861")
    version("7.1.0", sha256="7e9b36f6e7c01a5c8c4747340b3d0c064ce2e48c93fcfbfe45139854fae74103")
    version("6.1.1", sha256="ed46b7e062e0dfd8de671c7a5f6d120fb2b720982e918dbeb01e6985694c0273")
    version("5.0.1", sha256="9f755ddd08358be436f08b02df398e50e7508b856131aeeed235099bb3a7eba5")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@6.1.0:")
    depends_on("r@3.2:", type=("build", "run"), when="@7.1.0:")
    depends_on("r@3.3:", type=("build", "run"), when="@7.1.2:")
    depends_on("r@3.6:", type=("build", "run"), when="@7.3.0:")
    depends_on("r-brew", type=("build", "run"))
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@7.2.0:")
    depends_on("r-commonmark", type=("build", "run"))
    depends_on("r-desc@1.2.0:", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"), when="@7.1.0:")
    depends_on("r-pkgload@1.0.2:", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-purrr@0.3.3:", type=("build", "run"), when="@7.1.0:")
    depends_on("r-purrr@1.0.0:", type=("build", "run"), when="@7.3.0:")
    depends_on("r-r6@2.1.2:", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@7.1.0:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@7.2.0:")
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@7.2.3:")
    depends_on("r-stringi", type=("build", "run"))
    depends_on("r-stringr@1.0.0:", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"), when="@7.2.0:")
    depends_on("r-xml2", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"), when="@7.1.2:")

    depends_on("r-rcpp@0.11.0:", type=("build", "run"), when="@:7.1.1")
    depends_on("r-digest", type=("build", "run"), when="@:7.2.1")
