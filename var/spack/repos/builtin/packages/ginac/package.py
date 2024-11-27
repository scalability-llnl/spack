# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ginac(CMakePackage):
    """GiNaC is a C++ library. It is designed to allow the creation of
    integrated systems that embed symbolic manipulations together with more
    established areas of computer science (like computation-intense numeric
    applications, graphical interfaces, etc.) under one roof."""

    homepage = "https://www.ginac.de/"
    url = "https://www.ginac.de/ginac-1.7.8.tar.bz2"
    git = "git://www.ginac.de/ginac.git"

    license("GPL-2.0-or-later")

    version("1.7.11", sha256="96529ddef6ae9788aca0093f4b85fc4e34318bc6704e628e6423ab5a92dfe929")
    version("1.7.9", sha256="67cdff43a4360da997ee5323cce27cf313a5b17ba58f02e8f886138c0f629821")
    version("1.7.8", sha256="0c86501aa6c72efd5937fce42c5e983fc9f05dadb65b4ebdb51ee95c9f6a7067")

    variant("ginsh", default=True, description="Build ginsh, the GiNaC interactive shell")

    depends_on("cmake@2.8:", type="build")

    depends_on("cln")
    depends_on("python@3:", type=("build", "run"))
    depends_on("bison@2.3:", type=("build"), when="+ginsh")
    depends_on("flex@2.5.33:", type=("build"), when="+ginsh")
    depends_on("readline@4.3:", type=("link"), when="+ginsh")
