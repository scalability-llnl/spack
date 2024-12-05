# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRegistry(RPackage):
    """Infrastructure for R Package Registries.

    Provides a generic infrastructure for creating and using registries."""

    cran = "registry"

    license("GPL-2.0-only")

    version("0.5-1", sha256="dfea36edb0a703ec57e111016789b47a1ba21d9c8ff30672555c81327a3372cc")
    version("0.5", sha256="5d8be59ba791987b2400e9e8eaaac614cd544c1aece785ec4782ea6d5ea00efb")
    version("0.3", sha256="58a5c43b8012ca5e509fa29a8daf6f24f097b8eb021a723f6a9c33db1dd3f430")

    depends_on("r@2.6.0:", type=("build", "run"))
