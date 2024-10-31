# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kyotocabinet(AutotoolsPackage):
    """Kyoto Cabinet is a library of routines for managing a database."""

    homepage = "https://dbmx.net/kyotocabinet/"
    url = "https://dbmx.net/kyotocabinet/pkg/kyotocabinet-1.2.80.tar.gz"

    maintainers("EbiArnie")

    license("GPL-3.0-or-later")

    version("1.2.80", sha256="4c85d736668d82920bfdbdb92ac3d66b7db1108f09581a769dd9160a02def349")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api@1.2.3:", type=("build", "link"))
    depends_on("lzo", type=("build", "link"))
    depends_on("xz", type=("build", "link"))

    def configure_args(self):
        args = []

        args.append("--enable-lzo")
        args.append("--enable-lzma")

        return args
