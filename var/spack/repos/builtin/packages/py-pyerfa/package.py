# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyerfa(PythonPackage):
    """
    PyERFA is the Python wrapper for the ERFA library (Essential Routines for
    Fundamental Astronomy), a C library containing key algorithms for astronomy,
    which is based on the SOFA library published by the International Astronomical
    Union (IAU). All C routines are wrapped as Numpy universal functions, so that
    they can be called with scalar or array inputs.
    """

    homepage = "https://github.com/liberfa/pyerfa"
    pypi = "pyerfa/pyerfa-2.0.0.1.tar.gz"

    maintainers("meyersbs")

    license("BSD-3-Clause")

    version("2.0.1.1", sha256="dbac74ef8d3d3b0f22ef0ad3bbbdb30b2a9e10570b1fa5a98be34c7be36c9a6b")
    version("2.0.0.1", sha256="2fd4637ffe2c1e6ede7482c13f583ba7c73119d78bef90175448ce506a0ede30")

    depends_on("c", type="build")  # generated

    # From setup.cfg
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-numpy@1.25:2", when="@2.0.1.1", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.2:", when="@2.0.1.1", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    # From pyproject.toml
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-jinja2@2.10.3:", type="build")
