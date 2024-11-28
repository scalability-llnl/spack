# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycm(PythonPackage):
    """Multi-class confusion matrix library in Python."""

    homepage = "https://www.pycm.io"
    pypi = "pycm/pycm-4.0.tar.gz"

    license("MIT")

    version("4.0", sha256="839e217eeb9a093be633ea746c5ca8b7ab6591d978762face892473c9f28959d")

    depends_on("py-art@1.8:", type=("build", "run"))
    depends_on("py-numpy@1.9.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
