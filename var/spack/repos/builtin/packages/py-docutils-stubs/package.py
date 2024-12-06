# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocutilsStubs(PythonPackage):
    """PEP 561 based Type information for docutils."""

    homepage = "https://github.com/tk0miya/docutils-stubs"
    pypi = "docutils-stubs/docutils-stubs-0.0.21.tar.gz"

    license("Unlicense")

    version("0.0.21", sha256="e0d3d2588a0c0b47bf66b917bf4ff2c100cf4cf77bbe2f518d97b8f4d63e735c")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-docutils@0.14", type=("build", "run"))
