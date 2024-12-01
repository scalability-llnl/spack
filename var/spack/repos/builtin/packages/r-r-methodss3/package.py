# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRMethodss3(RPackage):
    """S3 Methods Simplified.

    Methods that simplify the setup of S3 generic functions and S3 methods.
    Major effort has been made in making definition of methods as simple as
    possible with a minimum of maintenance for package developers. For example,
    generic functions are created automatically, if missing, and naming
    conflict are automatically solved, if possible. The method setMethodS3() is
    a good start for those who in the future may want to migrate to S4. This is
    a cross-platform package implemented in pure R that generates standard S3
    methods."""

    cran = "R.methodsS3"

    version("1.8.2", sha256="822d5e61dad4c91e8883be2b38d7b89f87492046d0fe345704eb5d2658927c2e")
    version("1.8.1", sha256="8a98fb81bcfa78193450f855f614f6f64e6c65daf115f301d97d1f474f5e619b")
    version("1.7.1", sha256="44b840399266cd27f8f9157777b4d9d85ab7bd31bfdc143b3fc45079a2d8e687")

    depends_on("r@2.13.0:", type=("build", "run"))
