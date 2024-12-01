# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLatexcodec(PythonPackage):
    """A lexer and codec to work with LaTeX code in Python."""

    homepage = "https://latexcodec.readthedocs.io"
    pypi = "latexcodec/latexcodec-1.0.4.tar.gz"

    license("MIT")

    version("1.0.4", sha256="62bf8a3ee298f169a4d014dad5522bc1325b54dc98789a453fd338620387cb6c")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.4.1:", type=("build", "run"))
