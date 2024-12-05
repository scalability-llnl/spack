# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContextily(PythonPackage):
    """Context geo-tiles in Python."""

    homepage = "https://github.com/darribas/contextily"
    pypi = "contextily/contextily-1.0.1.tar.gz"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("1.0.1", sha256="f7dc25dbc8e01163be6cdeedb49a56da9cd0d586c838861f442ef2ee45eba9d4")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-geopy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-mercantile", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-rasterio", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
