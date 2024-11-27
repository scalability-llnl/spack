# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExodusBundler(PythonPackage):
    """Exodus is a tool that makes it easy to successfully relocate Linux
    ELF binaries from one system to another."""

    homepage = "https://github.com/intoli/exodus"
    pypi = "exodus-bundler/exodus-bundler-2.0.2.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("2.0.2", sha256="4e896a2034b94cf7b4fb33d86a68e29a7d3b08e57541e444db34dddc6ac1ef68")

    depends_on("c", type="build")  # generated

    depends_on("musl", type="run", when="%apple-clang")
    depends_on("musl", type="run", when="%clang")
    depends_on("musl", type="run", when="%gcc")
    depends_on("py-setuptools", type=("build", "run"))
