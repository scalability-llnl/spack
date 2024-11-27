# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonMarkdownMath(PythonPackage):
    """Math extension for Python-Markdown"""

    pypi = "python-markdown-math/python-markdown-math-0.8.tar.gz"

    maintainers("wscullin")

    license("BSD-3-Clause")

    version("0.8", sha256="8564212af679fc18d53f38681f16080fcd3d186073f23825c7ce86fadd3e3635")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools@30.3:", type="build")

    depends_on("py-markdown@3.0:", type=("build", "run"))
