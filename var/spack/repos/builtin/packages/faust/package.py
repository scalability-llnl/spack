# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Faust(MakefilePackage):
    """Faust (Functional Audio Stream) is a functional programming language
    specifically designed for real-time signal processing and synthesis.
    A distinctive characteristic of Faust is to be fully compiled."""

    homepage = "https://faust.grame.fr/"
    url = "https://github.com/grame-cncm/faust/archive/2.27.2.tar.gz"

    license("GPL-2.0-or-later")

    version("2.72.14", sha256="f0c82b7e72b663c29c226e5a56f6c43595b7d02c3d63eca0103cd327df4f33cd")
    version("2.70.3", sha256="644484f95167fe63014eac3db410f50c58810289fea228a2221e07d27da50eec")
    version("2.54.9", sha256="14648f020d77874e6f7411d7ff605820015645bbd4b891b24bee3d3a898e48d2")
    version("2.27.2", sha256="3367a868a93b63582bae29ab8783f1df7a10f4084a2bc1d2258ebf3d6a8c31d7")
    version("2.27.1", sha256="b3e93ca573025b231931e5eb92efc1a1e7f7720902aa3b285061519600a8c417")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake", type="build")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
