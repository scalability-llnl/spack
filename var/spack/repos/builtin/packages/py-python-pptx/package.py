# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPptx(PythonPackage):
    """Generate and manipulate Open XML PowerPoint (.pptx) files."""

    homepage = "https://github.com/scanny/python-pptx"
    pypi = "python-pptx/python-pptx-0.6.21.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("0.6.23", sha256="587497ff28e779ab18dbb074f6d4052893c85dedc95ed75df319364f331fedee")
    version("0.6.21", sha256="7798a2aaf89563565b3c7120c0acfe9aff775db0db3580544e3bf4840c2e378f")

    depends_on("py-setuptools", type="build")
    depends_on("py-lxml@3.1.0:", type=("build", "run"))
    depends_on("pil@3.3.2:", type=("build", "run"))
    depends_on("py-xlsxwriter@0.5.7:", type=("build", "run"))
