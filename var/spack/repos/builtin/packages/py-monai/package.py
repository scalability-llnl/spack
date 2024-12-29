# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMonai(PythonPackage):
    """AI Toolkit for Healthcare Imaging"""

    homepage = "https://monai.io/"
    url = "https://github.com/Project-MONAI/MONAI/archive/refs/tags/0.8.1.tar.gz"

    license("Apache-2.0", checked_by="qwertos")

    version("1.3.2", sha256="e370e1fcd78854fb22c2414fa7419c15ff5afce67b923ce666d0f12979015136")
    version("0.8.1", sha256="e1227e6406cc47c23f6846f617350879ceba353915b948d917bf4308b17ea861")
    version("0.8.0", sha256="a63df7d5a680d9641c223ea090ff843a7d6f20bdb62095bd44f3b0480a4706ed")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.8:", when="@1.2:", type=("build", "run"))
    depends_on("py-ninja", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-torch@1.6:", type=("build", "run"))
    depends_on("py-torch@1.9:", when="@1.3.2:", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@1.3.2:", type=("build", "run"))
