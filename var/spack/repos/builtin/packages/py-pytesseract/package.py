# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytesseract(PythonPackage):
    """Python-tesseract is an Optical Character Recognition (OCR) Tool for python."""

    homepage = "https://github.com/madmaze/pytesseract"
    pypi = "pytesseract/pytesseract-0.3.8.tar.gz"

    license("Apache-2.0")

    version("0.3.8", sha256="6148a01e4375760862e8f56ea718e22b5d13b281454df46ea8dac9807793fc5a")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("pil", type=("build", "run"))
