# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUncertainties(PythonPackage):
    """Transparent calculations with uncertainties on the quantities involved
    (aka error propagation); fast calculation of derivatives
    """

    homepage = "https://uncertainties-python-package.readthedocs.io/en/latest/"
    pypi = "uncertainties/uncertainties-3.1.4.tar.gz"

    license("BSD-3-Clause")

    version("3.1.7", sha256="80111e0839f239c5b233cb4772017b483a0b7a1573a581b92ab7746a35e6faab")
    version("3.1.6", sha256="7c4db5aaafd227e95485b61fba5d235dc8133aeecd98f8fc1224c038ce063e2d")
    version("3.1.4", sha256="63548a94899f2a51eeb89b640f6ac311f481a8016b37dce157186e44619bc968")

    variant("optional", default=False, description="Enable extra features involving numpy")
    variant("docs", default=False, description="Build with documentation")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-future", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"), when="+optional")
    depends_on("py-sphinx", type="build", when="+docs")
