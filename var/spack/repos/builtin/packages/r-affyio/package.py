# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyio(RPackage):
    """Tools for parsing Affymetrix data files.

    Routines for parsing Affymetrix data files based upon file format
    information. Primary focus is on accessing the CEL and CDF file
    formats."""

    bioc = "affyio"

    version("1.70.0", commit="95560567e27088863c64e868a8e5069fc725b8d7")
    version("1.68.0", commit="33080c5eeb14c0ca40f0d231706af4e0c2c1ef8b")
    version("1.66.0", commit="3a0b90704fc46cddd99a72b985a6bdb348f69b50")
    version("1.64.0", commit="aa7ce48f3f4110431f6f488d45961fde4019ffb0")
    version("1.60.0", commit="ee20528b32700e99768da48143d6d45c9a7bbe91")
    version("1.54.0", commit="c0e306e1805a556a1074d1af1acdd18e0a04477f")
    version("1.52.0", commit="9da725ac1098a22a370fa96eb03e51e4f6d5d963")
    version("1.50.0", commit="911ea4f8e4cdf7b649b87ef7ed1a5f5b111ef38a")
    version("1.48.0", commit="01727a4492c3a0d50453fc91892e04bf5f7fcadb")
    version("1.46.0", commit="977597f2772e08273d86579486f452170566c880")

    depends_on("c", type="build")  # generated

    depends_on("r@2.6.0:", type=("build", "run"))
    depends_on("r-zlibbioc", type=("build", "run"))
    depends_on("zlib-api")
