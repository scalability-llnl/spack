# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCiteprocPy(PythonPackage):
    """Citations and bibliography formatter."""

    homepage = "https://github.com/brechtm/citeproc-py"
    pypi = "citeproc-py/citeproc-py-0.6.0.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("0.6.0", sha256="d9e3a224f936fe2e5033b5d9ffdacab769cedb61d96c4e0cf2f0b488f1d24b4e")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-rnc2rng@2.6.1,2.6.3:", type="build")
    depends_on("py-lxml", type=("build", "run"))
