# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJacobi(PythonPackage):
    """Fast numerical derivatives for analytic functions
    with arbitrary round-off error and error propagation."""

    homepage = "https://github.com/hdembinski/jacobi"
    pypi = "jacobi/jacobi-0.9.2.tar.gz"

    maintainers("jonas-eschle")
    license("MIT", checked_by="jonas-eschle")

    version("0.9.2", sha256="c11f481663246ef1c2da915b9f9ab4ef229051fb14e0afc232d4668301320828")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-numpy", type=("build", "run"))
