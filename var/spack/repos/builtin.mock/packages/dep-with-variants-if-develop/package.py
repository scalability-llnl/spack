# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DepWithVariantsIfDevelop(Package):
    """Package that adds a dependency with many variants only at @develop"""

    homepage = "https://dev.null"

    version("develop")
    version("1.0")

    depends_on("dep-with-variants", when="@develop")
