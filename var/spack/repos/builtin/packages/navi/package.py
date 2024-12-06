# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Navi(Package):
    """An interactive cheatsheet tool for the command-line"""

    homepage = "https://github.com/denisidoro/navi"
    url = "https://github.com/denisidoro/navi/archive/refs/tags/v2.20.1.tar.gz"

    maintainers("delucca")

    license("Apache-2.0")

    version("2.20.1", sha256="92644677dc46e13aa71b049c5946dede06a22064b3b1834f52944d50e3fdb950")
    depends_on("rust")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
