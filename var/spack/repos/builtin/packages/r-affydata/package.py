# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffydata(RPackage):
    """Affymetrix Data for Demonstration Purpose.

    Example datasets of a slightly large size. They represent 'real world
    examples', unlike the artificial examples included in the package
    affy."""

    bioc = "affydata"

    version("1.48.0", commit="037b86c86c114761ff1bcca64ab4e0bcd68063d3")
    version("1.46.0", commit="870745b886df9f1fbbd6130d266c0ef96f3afa66")
    version("1.44.0", commit="f18304a356cee8cd7297bab362b13c40e50439df")
    version("1.42.0", commit="4b54c1206bedd27ff9be32affc999a279f4e96f0")
    version("1.38.0", commit="b5e843b2514789d0d87bea44d762c89a95314ee7")
    version("1.32.0", commit="c7cef93f6edd23024f4b1985b90e89058874c2bd")
    version("1.30.0", commit="d5408d84b37ebae73b40a448dd52baf7b4a13bea")
    version("1.28.0", commit="a106a5514c352bf0bbc624ded58a93886d4ce96f")
    version("1.26.0", commit="eb0a44a39990b361f9fb1094837ffafb320f39a9")
    version("1.24.0", commit="663991606507572f083232e2b393d901270291d4")

    depends_on("r@2.4.0:", type=("build", "run"))
    depends_on("r-affy@1.23.4:", type=("build", "run"))
