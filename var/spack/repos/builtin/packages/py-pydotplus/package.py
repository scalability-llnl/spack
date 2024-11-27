# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydotplus(PythonPackage):
    """Python interface to Graphviz's Dot language"""

    homepage = "https://pydotplus.readthedocs.io/"
    pypi = "pydotplus/pydotplus-2.0.2.tar.gz"

    license("MIT")

    version("2.0.2", sha256="91e85e9ee9b85d2391ead7d635e3d9c7f5f44fd60a60e59b13e2403fa66505c4")

    variant("docs", default=False, description="Build docs")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyparsing@2.0.1:", type=("build", "run"))
    depends_on("py-sphinx", type="build", when="+docs")
    depends_on("py-sphinx-rtd-theme", type="build", when="+docs")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
