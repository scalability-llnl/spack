# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNbstripout(PythonPackage):
    """Strips outputs from Jupyter and IPython notebooks."""

    homepage = "https://github.com/kynan/nbstripout"
    pypi = "nbstripout/nbstripout-0.6.1.tar.gz"

    license("MIT")

    version("0.6.1", sha256="9065bcdd1488b386e4f3c081ffc1d48f4513a2f8d8bf4d0d9a28208c5dafe9d3")

    depends_on("py-setuptools", type="build")
    depends_on("py-nbformat", type=("build", "run"))
