# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCombinat(RPackage):
    """combinatorics utilities.

    routines for combinatorics."""

    cran = "combinat"

    license("GPL-2.0-only")

    version("0.0-8", sha256="1513cf6b6ed74865bfdd9f8ca58feae12b62f38965d1a32c6130bef810ca30c1")
