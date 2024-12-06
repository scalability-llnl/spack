# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPdf2image(PythonPackage):
    """A python module that wraps the pdftoppm utility to convert PDF to PIL Image object"""

    homepage = "https://pypi.org/project/pdf2image/"
    pypi = "pdf2image/pdf2image-1.12.1.tar.gz"

    license("MIT")

    version("1.16.3", sha256="74208810c2cef4d9e347769b8e62a52303982ddb4f2dfd744c7ab4b940ae287e")
    version("1.12.1", sha256="a0d9906f5507192210a8d5d7ead63145e9dec4bccc4564b1fb644e923913c31c")

    depends_on("py-setuptools", type="build")

    depends_on("pil", type=("build", "run"))
    depends_on("poppler", type=("build", "run"))
