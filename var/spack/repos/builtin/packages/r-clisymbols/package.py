# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClisymbols(RPackage):
    """Unicode Symbols at the R Prompt.

    A small subset of Unicode symbols, that are useful when building command
    line applications. They fall back to alternatives on terminals that do not
    support Unicode. Many symbols were taken from the 'figures' 'npm' package
    (see <https://github.com/sindresorhus/figures>)."""

    cran = "clisymbols"

    license("MIT")

    version("1.2.0", sha256="0649f2ce39541820daee3ed408d765eddf83db5db639b493561f4e5fbf88efe0")
