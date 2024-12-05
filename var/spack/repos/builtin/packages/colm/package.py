# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Colm(AutotoolsPackage):
    """Colm Programming Language
    Colm is a programming language designed for the analysis and
    transformation of computer languages. Colm is influenced primarily
    by TXL. It is in the family of program transformation languages.
    """

    homepage = "https://www.colm.net/open-source/colm"
    url = "https://www.colm.net/files/colm/colm-0.12.0.tar.gz"

    license("GPL-2.0-only")

    version("0.12.0", sha256="7b545d74bd139f5c622975d243c575310af1e4985059a1427b6fdbb1fb8d6e4d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
