# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoatools(PythonPackage):
    """Python scripts to find enrichment of GO terms"""

    homepage = "https://github.com/tanghaibao/goatools"
    pypi = "goatools/goatools-0.7.11.tar.gz"

    license("BSD-2-Clause")

    version("0.7.11", sha256="753c6fb8c901367aa5d64ce5ad487d82903e424cf8ec7bac50ee069b307f6364")

    depends_on("py-setuptools", type="build")
    depends_on("py-nose", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pydot", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-pytest", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-statsmodels", type=("build", "run"))
    depends_on("py-xlrd", type=("build", "run"))
    depends_on("py-xlsxwriter", type=("build", "run"))
