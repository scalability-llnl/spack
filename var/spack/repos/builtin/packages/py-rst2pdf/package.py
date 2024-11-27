# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRst2pdf(PythonPackage):
    """Convert reStructured Text to PDF via ReportLab.

    The usual way of creating PDF from reStructuredText is by going through
    LaTeX. This tool provides an alternative by producing PDF directly using
    the ReportLab library."""

    homepage = "https://rst2pdf.org/"
    pypi = "rst2pdf/rst2pdf-0.99.tar.gz"
    git = "https://github.com/rst2pdf/rst2pdf.git"

    license("MIT")

    version("0.100", sha256="664c3c16e6d3dea274e840a436eac4dba6cb50ab6af3162fc9d5716be3cb7b42")
    version("0.99", sha256="8fa23fa93bddd1f52d058ceaeab6582c145546d80f2f8a95974f3703bd6c8152")

    depends_on("python@3.8:", when="@0.100:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-reportlab", type=("build", "run"))
    depends_on("py-smartypants", type=("build", "run"))
