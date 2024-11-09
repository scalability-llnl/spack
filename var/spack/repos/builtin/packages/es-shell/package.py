# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EsShell(AutotoolsPackage):
    """Es is an extensible shell. The language was derived from the Plan 9
    shell, rc, and was influenced by functional programming languages,
    such as Scheme, and the Tcl embeddable programming language. This
    implementation is derived from Byron Rakitzis's public domain
    implementation of rc."""

    homepage = "https://wryun.github.io/es-shell/"
    url = "https://github.com/wryun/es-shell/releases/download/v0.9.1/es-0.9.1.tar.gz"

    license("Public-Domain")

    version("0.9.1", sha256="b0b41fce99b122a173a06b899a4d92e5bd3cc48b227b2736159f596a58fff4ba")

    depends_on("c", type="build")  # generated

    depends_on("readline")
    depends_on("yacc")
