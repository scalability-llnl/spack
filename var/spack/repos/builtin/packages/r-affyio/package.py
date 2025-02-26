# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyio(RPackage):
    """Tools for parsing Affymetrix data files.

    Routines for parsing Affymetrix data files based upon file format
    information. Primary focus is on accessing the CEL and CDF file
    formats."""

    bioc = "affyio"

    version("1.76.0", commit="ed8b074ada05f3b3eeba3032b1214179e3034a42")
    version("1.74.0", commit="1d0948e7a76a00da985b9fdd38d36fa0ca85c2af")
    version("1.72.0", commit="2f97a7e3710e44886b0b732d1c0dbb3165e9b84c")
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
    depends_on("zlib-api")

    depends_on("r-zlibbioc", type=("build", "run"), when="@:1.77.0")
