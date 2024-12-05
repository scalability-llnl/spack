# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribTrio(PythonPackage):
    """This sphinx extension helps you document Python code that uses
    async/await, or abstract methods, or context managers, or generators,
    or ... you get the idea."""

    homepage = "https://github.com/python-trio/sphinxcontrib-trio"
    pypi = "sphinxcontrib-trio/sphinxcontrib-trio-1.1.2.tar.gz"

    license("Apache-2.0")

    version("1.1.2", sha256="9f1ba9c1d5965b534e85258d8b677dd94e9b1a9a2e918b85ccd42590596b47c0")
    version("1.1.0", sha256="d90f46d239ba0556e53d9a110989f98c9eb2cea76ab47937a1f39b62f63fe654")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.7:", type=("build", "run"))

    patch("sphinxcontrib-trio.patch", when="@1.1.0")
