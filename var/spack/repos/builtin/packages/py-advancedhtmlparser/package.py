# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAdvancedhtmlparser(PythonPackage):
    """Fast Indexed python HTML parser which builds a DOM node tree,
    providing common getElementsBy* functions for scraping, testing,
    modification, and formatting"""

    homepage = "https://github.com/kata198/AdvancedHTMLParser"
    pypi = "advancedhtmlparser/AdvancedHTMLParser-8.1.4.tar.gz"

    license("LGPL-3.0-or-later")

    version("9.0.1", sha256="1b7f632ca4c61fca50ee896c84112b97915c07d5b25b9527aefe7cbad8458837")
    version("8.1.4", sha256="21a73137026c8ec3248c654a24cc40064196029256cdf71681149f6835e9ed39")

    depends_on("py-setuptools", type="build")
    depends_on("py-queryablelist", type=("build", "run"))
