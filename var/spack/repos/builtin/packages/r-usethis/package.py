# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUsethis(RPackage):
    """Automate Package and Project Setup.

    Automate package and project setup tasks that are otherwise performed
    manually. This includes setting up unit testing, test coverage, continuous
    integration, Git, 'GitHub', licenses, 'Rcpp', 'RStudio' projects, and
    more."""

    cran = "usethis"

    license("MIT")

    version("3.0.0", sha256="98f850f9ceaae37eb16ccd1232275b4e8f818c115c67151fa99096c477f7ccb5")
    version("2.1.6", sha256="31dc6707577065ac1d4acb7d4cbf135942727c5cc2699092198c544be86f6818")
    version("2.1.5", sha256="7d539e16ecdc1cd45ba1a215d42d8b9c16bc38280ddd27048003dbb37b16f052")
    version("2.0.0", sha256="22aa2b59f36a8701a4648554c7b0e010253bf917a0f431f06efac7d8a6b59854")
    version("1.6.1", sha256="60339059a97ed07dea7f8908b828b5bb42e0fd0b471165c061bc9660b0d59d6f")
    version("1.5.1", sha256="9e3920a04b0df82adf59eef2c1b2b4d835c4a757a51b3c163b8fc619172f561d")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@2.1.5:")
    depends_on("r@3.6:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-cli", type=("build", "run"), when="@1.6.1:")
    depends_on("r-cli@3.0.1:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-clipr@0.3.0:", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-curl@2.7:", type=("build", "run"))
    depends_on("r-desc", type=("build", "run"))
    depends_on("r-desc@1.4.0:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-desc@1.4.2:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-fs@1.3.0:", type=("build", "run"))
    depends_on("r-gert@1.0.2:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-gert@1.4.1:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-gh", type=("build", "run"))
    depends_on("r-gh@1.1.0:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-gh@1.2.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-gh@1.2.1:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-glue@1.3.0:", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"), when="@2.0.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@2.0.0:")
    depends_on("r-lifecycle@1.0.0:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-rappdirs", type=("build", "run"), when="@2.0.0:")
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rlang@0.4.3:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@2.1.6:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@2.2.0:")
    depends_on("r-rprojroot@1.2:", type=("build", "run"))
    depends_on("r-rstudioapi", type=("build", "run"))
    depends_on("r-whisker", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-withr@2.3.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-yaml", type=("build", "run"))

    depends_on("r-clisymbols", type=("build", "run"), when="@:1.5")
    depends_on("r-git2r@0.23:", type=("build", "run"), when="@:1.6.1")
    depends_on("r-rematch2", type=("build", "run"), when="@1.6.1")
