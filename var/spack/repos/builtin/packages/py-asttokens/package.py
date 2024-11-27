# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsttokens(PythonPackage):
    """Annotate AST trees with source code positions."""

    homepage = "https://github.com/gristlabs/asttokens"
    pypi = "asttokens/asttokens-2.0.5.tar.gz"

    license("Apache-2.0")

    version("2.4.0", sha256="2e0171b991b2c959acc6c49318049236844a5da1d65ba2672c4880c1c894834e")
    version("2.2.1", sha256="4622110b2a6f30b77e1473affaa97e711bc2f07d3f10848420ff1898edbe94f3")
    version("2.0.8", sha256="c61e16246ecfb2cde2958406b4c8ebc043c9e6d73aaa83c941673b35e5d3a76b")
    version("2.0.5", sha256="9a54c114f02c7a9480d56550932546a3f1fe71d8a02f1bc7ccd0ee3ee35cf4d5")

    depends_on("py-setuptools@44:", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", type="build")

    depends_on("py-six@1.12:", when="@2.3:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
