# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygeos(PythonPackage):
    """PyGEOS is a C/Python library with vectorized geometry functions.

    The geometry operations are done in the open-source geometry library GEOS.
    PyGEOS wraps these operations in NumPy ufuncs providing a performance
    improvement when operating on arrays of geometries."""

    homepage = "https://github.com/pygeos/pygeos"
    pypi = "pygeos/pygeos-0.8.tar.gz"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version("0.14", sha256="30fbc17f64844200b85133b885fcfb65541b8779531f6ef4f8fe467d3fba7623")
    version("0.10", sha256="8ad4703cf8f983a6878a885765be975709a2fe300e54bc6c8623ddbca4903b6c")
    version("0.9", sha256="c0584b20e95f80ee57277a6eb1e5d7f86600f8b1ef3c627d238e243afdcc0cc7")
    version("0.8", sha256="45b7e1aaa5fc9ff53565ef089fb75c53c419ace8cee18385ec1d7c1515c17cbc")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-cython@0.29:0", when="@0.14:", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-setuptools@61:", when="@0.14:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.13:", when="@0.9:", type=("build", "link", "run"))
    depends_on("py-numpy@1.10:", type=("build", "link", "run"))
    depends_on("geos@3.5:")
