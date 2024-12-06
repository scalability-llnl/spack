# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyAsciidoctor(RubyPackage):
    """A fast, open source text processor and publishing toolchain for
    converting AsciiDoc content to HTML 5, DocBook 5, and other formats."""

    homepage = "https://asciidoctor.org/"
    url = "https://github.com/asciidoctor/asciidoctor/archive/v2.0.10.tar.gz"

    license("MIT")

    version("2.0.17", sha256="ca939b978d5d3bfe0cfcf1bcf5513f199aa77813e4a19f568dc6b6f17b892728")
    version("2.0.10", sha256="afca74837e6d4b339535e8ba0b79f2ad00bd1eef78bf391cc36995ca2e31630a")

    depends_on("ruby@2.3.0:", type=("build", "run"))
