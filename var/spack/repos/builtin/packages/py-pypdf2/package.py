# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPypdf2(PythonPackage):
    """PyPDF2 is a free and open source pure-python PDF library capable of
    splitting, merging, cropping, and transforming the pages of PDF files.
    It can also add custom data, viewing options, and passwords to PDF files.
    PyPDF2 can retrieve text and metadata from PDFs as well."""

    homepage = "https://pypdf2.readthedocs.io/en/latest/"
    pypi = "PyPDF2/PyPDF2-2.5.0.tar.gz"

    version("2.5.0", sha256="5802b1f40fa79be1b5ab9edc95a4e7f7e73399589db4f0e66ca831f449e7a2cd")
    version("1.26.0", sha256="e28f902f2f0a1603ea95ebe21dff311ef09be3d0f0ef29a3e44a932729564385")

    depends_on("python@3.6:", type=("build", "run"), when="@2.0.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions", type=("build", "run"), when="@2.0.0:^python@:3.9")
