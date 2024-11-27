# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymbolic(PythonPackage):
    """A simple package to do symbolic math (focus on code gen and DSLs)"""

    homepage = "http://mathema.tician.de/software/pymbolic"
    pypi = "pymbolic/pymbolic-2022.2.tar.gz"
    git = "https://github.com/inducer/pymbolic.git"

    maintainers("cgcgcg")

    license("MIT")

    version("2022.2", sha256="f82776942bb3cb72329fa1f1aa2b68ec09f237db9178c95cfdc92a6aea7cec89")

    depends_on("python@3.8:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytools@2:", type="run")
