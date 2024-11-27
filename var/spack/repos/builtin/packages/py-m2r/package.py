# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyM2r(PythonPackage):
    """M2R converts a markdown file including reStructuredText (rst) markups to
    a valid rst format."""

    homepage = "https://github.com/miyakogi/m2r"
    url = "https://github.com/miyakogi/m2r/archive/v0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="9286c1a5d7548f34b0a12017444e4c441781bef4b71f321f723e314b76b6c498")
    version("0.2.0", sha256="e9b7476203c4a5e3b822eb0ef110011d7b427d2c0dbdc4030f9cbcd239fbd4d6")
    version("0.1.15", sha256="4ca4c73385512f6e54db8e152ba157fc3eea84f9e942fe60a12ace5078ff83df")
    version("0.1.14", sha256="d8f844cc6f0c954e55eb3d599e436b337e7f97559dafa7ff54412a5f06f0867c")
    version("0.1.13", sha256="97f81a45b922f7700e0c0dfd742c79d904e337e92ec4241a11aa579713a1afa4")
    version("0.1.12", sha256="585b5b4e30494858de49ad844cafeb752bd12764fd6c20ca8496ddd4be5e8d21")
    version("0.1.11", sha256="a29ef03a0b67116ba8e394a4b3f8afc354211b899f89dedf9c4c0b79828e9ca7")
    version("0.1.10", sha256="4c7a92f111ac842b9c4d3719b8d785b26cb1cf6e81ec0940f8fe0ccc078e6925")
    version("0.1.9", sha256="86fe3c8c54a59807e0ef8cfe5a79fc013b4aaced1f3db493878f5ec1a46bb6d5")
    version("0.1.8", sha256="2bfeb2f3de5f9fe9cd411aba82767a6473a43db96ca1730c03b0fe0167239b7e")

    depends_on("py-setuptools", type="build")
    depends_on("py-mistune@:1", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
