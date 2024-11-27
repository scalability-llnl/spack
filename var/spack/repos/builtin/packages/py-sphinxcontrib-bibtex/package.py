# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribBibtex(PythonPackage):
    """A Sphinx extension for BibTeX style citations."""

    pypi = "sphinxcontrib-bibtex/sphinxcontrib-bibtex-0.3.5.tar.gz"

    version("2.5.0", sha256="71b42e5db0e2e284f243875326bf9936aa9a763282277d75048826fef5b00eaa")
    version("2.4.2", sha256="65b023ee47f35f1f03ac4d71c824e67c624c7ecac1bb26e83623271a01f9da86")
    version("2.2.1", sha256="00d474092e04b1d941e645cf6c027632a975cd0b9337cf47d379f63a5928f334")
    version("2.2.0", sha256="7500843e154d76983c23bca5ca7380965e0725c46b8f484c1322d0b58a6ce3b2")
    version("2.1.4", sha256="f53ec0cd534d2c8f0a51b4b3473ced46e9cb0dd99a7c5019249fe0ef9cbef18e")
    version("2.0.0", sha256="98e18eb0b088d3f556199f3fbb91d3d48ebb7596fe86b6c37cc4c4dc5419b7a1")
    version("1.0.0", sha256="629612b001f86784669d65e662377a482052decfd9a0a17c46860878eef7b9e0")
    version("0.3.5", sha256="c93e2b4a0d14f0ab726f95f0a33c1675965e9df3ed04839635577b8f978206cd")

    depends_on("python@3.5:", type=("build", "run"), when="@1:")
    depends_on("python@3.6:", type=("build", "run"), when="@2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-latexcodec@0.3.0:", type=("build", "run"), when="@:0.3.6")
    depends_on("py-pybtex@0.17:", type=("build", "run"), when="@:1")
    depends_on("py-pybtex@0.20:", type=("build", "run"), when="@2:2.3")
    depends_on("py-pybtex@0.24:", type=("build", "run"), when="@2.4:")
    depends_on("py-pybtex-docutils@0.2.0:", type=("build", "run"), when="@:1")
    depends_on("py-pybtex-docutils@0.2.2:", type=("build", "run"), when="@2:")
    depends_on("py-pybtex-docutils@1.0.0:", type=("build", "run"), when="@2.2:")
    depends_on("py-six@1.4.1:", type=("build", "run"), when="@0.3.5")
    depends_on("py-sphinx@1.0:", type=("build", "run"), when="@:1")
    depends_on("py-sphinx@2.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("py-sphinx@2.1:", type=("build", "run"), when="@2.1.3:")
    depends_on("py-oset@0.1.3:", type=("build", "run"), when="@:2.0.0")
    depends_on("py-docutils@0.8:", type=("build", "run"), when="@2.1.0:")
    depends_on("py-importlib-metadata@3.6:", when="@2.5.0: ^python@:3.9", type=("build", "run"))
