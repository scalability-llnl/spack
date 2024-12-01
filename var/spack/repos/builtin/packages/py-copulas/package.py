# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCopulas(PythonPackage):
    """Copulas is a Python library for modeling multivariate
    distributions and sampling from them using copula
    functions. Given a table containing numerical data, we can
    use Copulas to learn the distribution and later on generate
    new synthetic rows following the same statistical
    properties."""

    homepage = "https://github.com/sdv-dev/Copulas"
    pypi = "copulas/copulas-0.6.0.tar.gz"

    license("MIT")

    version("0.6.0", sha256="9de6cc738769db19794fc18e2f506a4b5ee17e6902519c0842a4698c0efb6749")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@3.2:3", type=("build", "run"))
    depends_on("py-numpy@1.20:1", type=("build", "run"))
    depends_on("py-pandas@1.1.3:1", type=("build", "run"))
    depends_on("py-scipy@1.5.4:1", type=("build", "run"))
