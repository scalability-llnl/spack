# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Andi(AutotoolsPackage):
    """andi is used for for estimating the
    evolutionary distance between closely related genomes."""

    homepage = "https://github.com/EvolBioInf/andi"
    url = "https://github.com/EvolBioInf/andi/archive/v0.10.tar.gz"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("0.14", sha256="2c9e11524f38e74fe3f981e6acd9527c1a1ca30994a30c5e86808ba5165a25b7")
    version("0.10", sha256="1ff371de0b6db4080e402ded2687947dc2d6913e28626edec21dcf5149489ee8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("gsl")
    depends_on("libdivsufsort")
