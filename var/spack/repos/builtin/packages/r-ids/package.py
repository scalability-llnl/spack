# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIds(RPackage):
    """Generate Random Identifiers.

    Generate random or human readable and pronounceable identifiers."""

    cran = "ids"

    license("MIT")

    version("1.0.1", sha256="b6212a186063c23116c5cbd3cca65dbb8977dd737261e4526ebee8f64852cfe8")

    depends_on("r-openssl", type=("build", "run"))
    depends_on("r-uuid", type=("build", "run"))
