# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCmdstanr(RPackage):
    """R Interface to 'CmdStan'.

    A lightweight interface to 'Stan' <https://mc-stan.org>.  The 'CmdStanR'
    interface is an alternative to 'RStan' that calls the command line
    interface for compilation and running algorithms instead of interfacing
    with C++ via 'Rcpp'. This has many benefits including always being
    compatible with the latest version of Stan, fewer installation errors,
    fewer unexpected crashes in RStudio, and a more permissive license."""

    homepage = "https://mc-stan.org/cmdstanr/"
    url = "https://github.com/stan-dev/cmdstanr/archive/refs/tags/v0.5.3.tar.gz"

    license("BSD-3-Clause")

    version("0.5.3", sha256="dafd5808e1a17d2e4ae4048437235b4399464a7c65de68ba4af0ab2b03e27871")
    version("0.5.2", sha256="5bc2e164e7cce3bfb93d592df5e3059157c8d510b136535bdb6d09c3ef060f64")
    version("0.5.1", sha256="5b3e83d48c19d309ccca720979449a8ac130ba7e443e70992b1771a1dd9124c9")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-checkmate", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-jsonlite@1.2.0:", type=("build", "run"))
    depends_on("r-posterior@1.1.0:", type=("build", "run"))
    depends_on("r-processx@3.5.0:", type=("build", "run"))
    depends_on("r-r6@2.4.0:", type=("build", "run"))
    depends_on("r-withr@2.5.0:", type=("build", "run"), when="@0.5.2:")
    depends_on("cmdstan", type="run")
