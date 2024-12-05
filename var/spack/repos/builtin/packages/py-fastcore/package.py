# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastcore(PythonPackage):
    """Python is a powerful, dynamic language. Rather than bake
    everything into the language, it lets the programmer
    customize it to make it work for them. fastcore uses this
    flexibility to add to Python features inspired by other
    languages we've loved, like multiple dispatch from Julia,
    mixins from Ruby, and currying, binding, and more from
    Haskell. It also adds some "missing features" and clean up
    some rough edges in the Python standard library, such as
    simplifying parallel processing, and bringing ideas from
    NumPy over to Python's list type."""

    homepage = "https://github.com/fastai/fastcore/tree/master/"
    pypi = "fastcore/fastcore-1.3.27.tar.gz"

    license("Apache-2.0")

    version("1.3.27", sha256="0161f538d5b913932869a46bb90e98193eee79b8798b566272a394f7ef957243")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-packaging", type="build")
