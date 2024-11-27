# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHistoprint(PythonPackage):
    """Pretty print of NumPy (and other) histograms to the console"""

    homepage = "https://github.com/scikit-hep/histoprint"
    pypi = "histoprint/histoprint-2.2.0.tar.gz"

    license("MIT")

    version("2.4.0", sha256="328f789d186e3bd76882d57b5aad3fa08c7870a856cc83bcdbad9f4aefbda94d")
    version("2.2.0", sha256="ef8b65f7926aaa989f076857b76291175245dd974804b408483091d1e28b00f6")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-click@7.0.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-uhi@0.2.1:", type=("build", "run"))
