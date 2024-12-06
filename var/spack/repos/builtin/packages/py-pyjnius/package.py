# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyjnius(PythonPackage):
    """Pyjnius is a Python library for accessing Java classes."""

    homepage = "https://pyjnius.readthedocs.io/en/stable"
    pypi = "pyjnius/pyjnius-1.3.0.0.tar.gz"

    license("MIT")

    version("1.3.0.0", sha256="d20845e75a2d18224e661d0e2bc2ce9141f17472e685cd6579847b0a7b5da6ad")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six@1.7:", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("java", type=("build", "run"))
