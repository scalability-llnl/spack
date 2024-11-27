# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPureEval(PythonPackage):
    """Safely evaluate AST nodes without side effects."""

    homepage = "https://github.com/alexmojaki/pure_eval"
    git = "https://github.com/alexmojaki/pure_eval.git"
    pypi = "pure_eval/pure_eval-0.2.2.tar.gz"

    license("MIT")

    version("master", branch="master")
    version("0.2.2", sha256="2b45320af6dfaa1750f543d714b6d1c520a1688dec6fd24d339063ce0aaa9ac3")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools@44:", type="build")
    depends_on("py-setuptools-scm+toml@3.4.3:", type="build")
