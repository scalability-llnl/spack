# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpectra(PythonPackage):
    """Color scales and color conversion made easy for Python."""

    pypi = "spectra/spectra-0.0.8.tar.gz"

    license("MIT")

    version("0.0.11", sha256="8eb362a5187cb63cee13cd01186799c0c791a3ad3bec57b279132e12521762b8")
    version("0.0.8", sha256="851b88c9c0bba84e0be1fce5b9c02a7b4ef139a2b3e590b0d082d679e19f0759")

    depends_on("py-setuptools", type="build")
    depends_on("py-colormath", type=("build", "run"))
    depends_on("py-colormath@3.0.0:", type=("build", "run"), when="@0.0.11:")
