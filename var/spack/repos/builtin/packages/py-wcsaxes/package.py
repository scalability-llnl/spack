# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWcsaxes(PythonPackage):
    """WCSAxes is a framework for making plots of Astronomical data
    in Matplotlib."""

    homepage = "https://wcsaxes.readthedocs.io/en/latest/index.html"
    url = "https://github.com/astrofrog/wcsaxes/archive/v0.8.tar.gz"

    license("BSD-3-Clause")

    version("0.8", sha256="9c6addc1ec04cc99617850354b2c03dbd4099d2e43b45a81f8bc3069de9c8e83")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-astropy", type=("build", "run"))
