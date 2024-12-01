# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibcst(PythonPackage):
    """A Concrete Syntax Tree (CST) parser and serializer library for Python."""

    homepage = "https://github.com/Instagram/LibCST"
    pypi = "libcst/libcst-0.4.9.tar.gz"

    license("Apache-2.0")

    version("0.4.9", sha256="01786c403348f76f274dbaf3888ae237ffb73e6ed6973e65eba5c1fc389861dd")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-rust", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-typing-extensions@3.7.4.2:", type=("build", "run"))
    depends_on("py-typing-inspect@0.4:", type=("build", "run"))
    depends_on("py-pyyaml@5.2:", type=("build", "run"))
