# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hyphen(AutotoolsPackage):
    """A library of text hyphenation."""

    homepage = "https://hunspell.github.io"
    url = "https://downloads.sourceforge.net/hunspell/hyphen-2.8.8.tar.gz"
    git = "https://github.com/hunspell/hyphen.git"

    version("master", branch="master")
    version("2.8.8", sha256="304636d4eccd81a14b6914d07b84c79ebb815288c76fe027b9ebff6ff24d5705")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
