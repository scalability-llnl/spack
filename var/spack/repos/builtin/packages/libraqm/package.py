# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libraqm(MesonPackage):
    """Raqm provides a convenient API for the logic of complex text layout."""

    homepage = "https://github.com/HOST-Oman/libraqm"
    url = "https://github.com/HOST-Oman/libraqm/releases/download/v0.9.0/raqm-0.9.0.tar.xz"
    git = "https://github.com/HOST-Oman/libraqm.git"

    license("MIT")

    version("0.9.0", sha256="9ed6fdf41da6391fc9bf7038662cbe412c330aa6eb22b19704af2258e448107c")

    depends_on("c", type="build")  # generated

    variant(
        "bidi_algo",
        default="fribidi",
        description="Unicode Bidirectional Algorithm",
        values=("fribidi", "sheenbidi"),
        multi=False,
    )

    depends_on("freetype")
    depends_on("harfbuzz")

    depends_on("fribidi@1.0.6:", when="bidi_algo=fribidi")
    depends_on("sheenbidi@2.6:", when="bidi_algo=sheenbidi")
