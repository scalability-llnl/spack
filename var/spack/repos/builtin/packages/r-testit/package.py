# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RTestit(RPackage):
    """A Simple Package for Testing R Packages.

    Provides two convenience functions assert() and test_pkg() to facilitate
    testing R packages."""

    cran = "testit"

    license("GPL-3.0-only")

    version("0.13", sha256="90d47168ab6bdbd1274b600b457626ac07697ce09792c92b2043be5f5b678d80")
    version("0.12", sha256="9acdf912f0e7a68a5b6a7946d5ebb0c2007b3d6cd2e39075eddae2b586354e89")
    version("0.9", sha256="9cf6b3df9b2c700e4e7dcbd5b8cb64fabefe674e1f40346ccaf39fe7feda5e55")
    version("0.8", sha256="08a9c19c962eae60f4ab58885a23e0bc239efc39da682290be436c066f8d97f7")
    version("0.7", sha256="03332889bffe8b69d36e696e3a6a1a29713cdcbccf1efced6cddbf061fb41a1f")
    version("0.5", sha256="1416fd69b324e5049be5adfaebde159252a119e8e987562e48b4b28cc9af69ec")
