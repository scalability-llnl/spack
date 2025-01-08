# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMaptools(RPackage):
    """Tools for Handling Spatial Objects.

    Set of tools for manipulating and reading geographic data, in particular
    ESRI shapefiles; C code used from shapelib. It includes binary access to
    GSHHG shoreline files. The package also provides interface wrappers for
    exchanging spatial objects with packages such as PBSmapping, spatstat,
    maps, RArcInfo, Stata tmap, WinBUGS, Mondrian, and others."""

    cran = "maptools"

    version("1.1-8", sha256="5e8579e3f559161935f1dde622ece703eefa2a28a677ce553d7f27611e66e0f7")
    version(
        "1.1-6",
        sha256="d6a5df52db03b2231f21921b693c67f85df3c3b376181aa13ef4f21710f69308",
        deprecated=True,
    )
    version(
        "1.1-5",
        sha256="3cd9bd95d3a1cb4aae3a350e0582319dacc25f070af6995061b85e68042f25dc",
        deprecated=True,
    )
    version(
        "1.1-4",
        sha256="f3ee25f9787d97c8373dac3651c6a198c932948eb3a6006b8618c91c6344fdc9",
        deprecated=True,
    )
    version(
        "1.1-2",
        sha256="3995c96e8472cd6717fe3cbd3506358ff460b6c2cf92dbe4b00f75f507514439",
        deprecated=True,
    )
    version(
        "1.0-2",
        sha256="daac6da5817cf0cff17b9e7d4a7cdc7c329574249bd9b1bafdb6c9431e1fee49",
        deprecated=True,
    )
    version(
        "0.9-5",
        sha256="5d9511f09fb49d57a51f28495b02239800596a4fcfad7b03ee1074d793657bdd",
        deprecated=True,
    )
    version(
        "0.9-4",
        sha256="930875f598a516f0f9049fa2fae7391bc9bdf7e3e5db696059ab4ec2fc9ba39c",
        deprecated=True,
    )
    version(
        "0.8-39",
        sha256="4b81e313e45dbb75e0fbb180b02985d1c34aaa5669e483283b632788e6a67dd2",
        deprecated=True,
    )

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-sp@1.0-11:", type=("build", "run"))
    depends_on("r-foreign@0.8:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
