# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPdoc3(PythonPackage):
    """Auto-generate API documentation for Python projects."""

    homepage = "https://pdoc3.github.io/pdoc/"
    pypi = "pdoc3/pdoc3-0.10.0.tar.gz"

    license("AGPL-3.0")

    version("0.10.0", sha256="5f22e7bcb969006738e1aa4219c75a32f34c2d62d46dc9d2fb2d3e0b0287e4b7")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-git", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-mako", type=("build", "run"))
    depends_on("py-markdown@3.0:", type=("build", "run"))
