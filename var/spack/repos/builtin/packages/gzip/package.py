# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Gzip(AutotoolsPackage):
    """GNU Gzip is a popular data compression program originally written by
    Jean-loup Gailly for the GNU project."""

    homepage = "https://www.gnu.org/software/gzip/"
    url = "https://ftp.gnu.org/gnu/gzip/gzip-1.10.tar.gz"

    license("GPL-3.0-or-later")

    version("1.13", sha256="20fc818aeebae87cdbf209d35141ad9d3cf312b35a5e6be61bfcfbf9eddd212a")
    version(
        "1.12",
        sha256="5b4fb14d38314e09f2fc8a1c510e7cd540a3ea0e3eb9b0420046b82c3bf41085",
        deprecated=True,
    )
    version(
        "1.11",
        sha256="3e8a0e0c45bad3009341dce17d71536c4c655d9313039021ce7554a26cd50ed9",
        deprecated=True,
    )
    version(
        "1.10",
        sha256="c91f74430bf7bc20402e1f657d0b252cb80aa66ba333a25704512af346633c68",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    # Gzip makes a recursive symlink if built in-source
    build_directory = "spack-build"
