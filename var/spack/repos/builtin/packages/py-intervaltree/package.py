# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIntervaltree(PythonPackage):
    """Editable interval tree data structure for Python 2 and 3."""

    homepage = "https://github.com/chaimleib/intervaltree"
    url = "https://github.com/chaimleib/intervaltree/archive/3.0.2.tar.gz"

    license("Apache-2.0")

    version("3.0.2", sha256="e8ab75b66077f2e5fb85ac56cb6df834689edb048d38601d53d8867cce3b77d1")
    version("2.1.0", sha256="e444398cbc9582a51c372a344cc7e05d53c53daaac2aae827951ff88554b96ff")

    depends_on("py-sortedcontainers", type=("build", "run"))
    depends_on("py-sortedcontainers@2.0:2", when="@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
