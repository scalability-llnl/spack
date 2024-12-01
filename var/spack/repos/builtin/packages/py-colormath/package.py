# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColormath(PythonPackage):
    """Color math and conversion library."""

    pypi = "colormath/colormath-2.1.1.tar.gz"

    license("BSD-3-Clause")

    version("3.0.0", sha256="3d4605af344527da0e4f9f504fad7ddbebda35322c566a6c72e28edb1ff31217")
    version("2.1.1", sha256="003a2b2d9c1f43aa7d90addf1863fb2d822463c839b1166ae3092950792f9707")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-networkx@2.0:", type=("build", "run"), when="@3.0.0:")
