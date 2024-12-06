# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAneufinderdata(RPackage):
    """WGSCS Data for Demonstration Purposes.

    Whole-genome single cell sequencing data for demonstration purposes in
    the AneuFinder package."""

    bioc = "AneuFinderData"

    version("1.28.0", commit="d04255e60173ce478d31b1e1e5c73e6ed9e3b20c")
    version("1.26.0", commit="4b810599b62a3fb39239bfd98ed960c93989e86b")
    version("1.24.0", commit="cf6f3852702aab28e3170fc56b695d00b7389666")
    version("1.22.0", commit="ae8eec3b0afdc351dc447aad2024df5b2c75e56b")
    version("1.18.0", commit="1bf1657b28fc8c1425e611980a692da952ce3d1e")
    version("1.12.0", commit="7350f38856b6278e07eca141f7f3cb24bc60c3a1")
    version("1.10.0", commit="ef7fc27f9af4f178fa45a21aba30709e1ebde035")
    version("1.8.0", commit="4f00f8d5f2e968fea667a7feafc0a4607d6e0c6e")
    version("1.6.0", commit="8fe5b221619aab75fe84c9094708d240dd1e6730")
    version("1.4.0", commit="55c8807ee4a37a2eb6d0defafaf843f980b22c40")

    depends_on("r@3.3:", type=("build", "run"))
