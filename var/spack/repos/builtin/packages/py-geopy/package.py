# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopy(PythonPackage):
    """geopy is a Python client for several popular geocoding web services."""

    homepage = "https://github.com/geopy/geopy"
    pypi = "geopy/geopy-2.1.0.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version("2.1.0", sha256="892b219413e7955587b029949af3a1949c6fbac9d5ad17b79d850718f6a9550f")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-geographiclib@1.49:1", type=("build", "run"))
