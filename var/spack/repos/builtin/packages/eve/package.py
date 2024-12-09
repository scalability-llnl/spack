# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eve(CMakePackage):
    """Expressive Velocity Engine - SIMD in C++ Goes Brrrr"""

    homepage = "https://jfalcou.github.io/eve/"
    url = "https://github.com/jfalcou/eve/archive/refs/tags/v2023.02.15.tar.gz"
    maintainers("jfalcou")
    git = "https://github.com/jfalcou/eve.git"

    license("BSL-1.0")

    version("main", branch="main")
    version(
        "2023.02.15", sha256="7a5fb59c0e6ef3bef3e8b36d62e138d31e7f2a9f1bdfe95a8e96512b207f84c5"
    )
    version("2022.09.1", sha256="d8d3ae55f0ca2690f8a22883eaaa8251275b76702da0267e8e1725b22c51e978")
    version("2022.09.0", sha256="53a4e1944a1080c67380a6d7f4fb42998f1c1db35e2370e02d7853c3ac1e0a33")
    version("2022.03.0", sha256="8bf9faea516806e7dd468e778dcedc81c51f0b2c6a70b9c75987ce12bb759911")
    version("2021.10.0", sha256="580c40a8244039a700b93ea49fb0affc1c8d3c100eb6dc66368e101753f51e5c")

    depends_on("cxx", type="build")  # generated
