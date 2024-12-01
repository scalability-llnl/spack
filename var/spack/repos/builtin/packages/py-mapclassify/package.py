# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMapclassify(PythonPackage):
    """Classification Schemes for Choropleth Maps."""

    homepage = "https://github.com/pysal/mapclassify"
    pypi = "mapclassify/mapclassify-2.4.2.tar.gz"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("2.4.2", sha256="bc20954aa433466f5fbc572e3f23b05f9606b59209f40b0ded93ac1ca983d24e")

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy@1.0:", type=("build", "run"))
    depends_on("py-numpy@1.3:", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-pandas@1.0:", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
