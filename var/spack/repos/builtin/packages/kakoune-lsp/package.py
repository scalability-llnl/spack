# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class KakouneLsp(CargoPackage):
    """Kakoune Language Server Protocol Client"""

    homepage = "https://github.com/kakoune-lsp/kakoune-lsp"
    url = "https://github.com/kakoune-lsp/kakoune-lsp/archive/refs/tags/v17.0.1.tar.gz"

    maintainers("taliaferro")

    license("UNLICENSE", checked_by="taliaferro")

    version("17.0.1", sha256="c32172a7d13621d7f7fd8b32b819865fd58a38c0c431d3cedd6046fb6de42f44")
