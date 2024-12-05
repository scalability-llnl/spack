# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMarkdown2(PythonPackage):
    """A fast and complete Python implementation of Markdown."""

    homepage = "https://github.com/trentm/python-markdown2"
    pypi = "markdown2/markdown2-2.3.9.tar.gz"

    license("MIT")

    version("2.4.0", sha256="28d769f0e544e6f68f684f01e9b186747b079a6927d9ca77ebc8c640a2829b1b")

    depends_on("python@3.5:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
