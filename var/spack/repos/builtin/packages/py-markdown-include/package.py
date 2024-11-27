# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarkdownInclude(PythonPackage):
    """This is an extension to Python-Markdown which provides an "include"
    function, similar to that found in LaTeX (and also the
    C pre-processor and Fortran)."""

    pypi = "markdown-include/markdown-include-0.6.0.tar.gz"

    maintainers("wscullin")

    version("0.6.0", sha256="6f5d680e36f7780c7f0f61dca53ca581bd50d1b56137ddcd6353efafa0c3e4a2")

    depends_on("py-setuptools", type="build")

    depends_on("py-markdown", type=("build", "run"))
