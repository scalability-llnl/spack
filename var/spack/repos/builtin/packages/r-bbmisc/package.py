# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBbmisc(RPackage):
    """Miscellaneous Helper Functions for B. Bischl.

    Miscellaneous helper functions for and from B. Bischl and some other guys,
    mainly for package development."""

    cran = "BBmisc"

    version("1.13", sha256="1145dcf9fed15e7beeaa4a5c7075d8a8badd17c8246838cd63e40cd9551e4405")
    version("1.12", sha256="900a633f69b7d9b13d58709eeae2fca2c1bc510765d778623a2af32cc870053e")
    version("1.11", sha256="1ea48c281825349d8642a661bb447e23bfd651db3599bf72593bfebe17b101d2")

    depends_on("c", type="build")  # generated

    depends_on("r-checkmate@1.8.0:", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"), when="@1.12:")
