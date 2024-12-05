# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygps(PythonPackage):
    """pyGPs is a Python library for Gaussian Process (GP)
    Regression and Classification."""

    homepage = "https://github.com/marionmari/pyGPs"
    pypi = "pygps/pyGPs-1.3.5.tar.gz"

    license("DOC")

    version("1.3.5", sha256="5af668415a7bf1666c7c6da3bb09d29e48c395862c6feb23964b476972a015d4")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@0.13:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
