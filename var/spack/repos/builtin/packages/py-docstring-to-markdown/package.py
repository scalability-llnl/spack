# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocstringToMarkdown(PythonPackage):
    """On the fly conversion of Python docstrings to markdown."""

    homepage = "https://github.com/python-lsp/docstring-to-markdown"
    pypi = "docstring-to-markdown/docstring-to-markdown-0.10.tar.gz"

    maintainers("alecbcs")

    license("LGPL-2.1-or-later")

    version("0.11", sha256="5b1da2c89d9d0d09b955dec0ee111284ceadd302a938a03ed93f66e09134f9b5")
    version("0.10", sha256="12f75b0c7b7572defea2d9e24b57ef7ac38c3e26e91c0e5547cfc02b1c168bf6")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
