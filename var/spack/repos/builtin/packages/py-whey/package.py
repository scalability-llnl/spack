# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyWhey(PythonPackage):
    """A simple Python wheel builder for simple projects."""

    homepage = "https://github.com/repo-helper/whey"
    pypi = "whey/whey-0.0.24.tar.gz"

    license("MIT")

    version("0.0.24", sha256="411905d85aa8aa239733818894e08dc20b682f0a3614f942aa35b430db568aa2")

    depends_on("py-wheel@0.34.2", type="build")
    depends_on("py-setuptools@40.6:", type="build")

    conflicts("^py-setuptools@61")

    depends_on("py-click@7.1.2:", type=("build", "run"))
    depends_on("py-consolekit@1.4.1:", type=("build", "run"))
    depends_on("py-dist-meta@0.1:", type=("build", "run"))
    depends_on("py-dom-toml@0.4:", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.8:", type=("build", "run"))
    depends_on("py-handy-archives@0.1:", type=("build", "run"))
    depends_on("py-natsort@7.1.1:", type=("build", "run"))
    depends_on("py-packaging@20.9:", type=("build", "run"))
    depends_on("py-pyproject-parser@0.6:", type=("build", "run"))
    depends_on("py-shippinglabel@0.16:", type=("build", "run"))
