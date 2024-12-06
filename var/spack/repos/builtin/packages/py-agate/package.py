# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgate(PythonPackage):
    """agate is a Python data analysis library that is optimized for humans
    instead of machines. It is an alternative to numpy and pandas that solves
    real-world problems with readable code."""

    homepage = "https://agate.readthedocs.io/en/latest/"
    pypi = "agate/agate-1.6.1.tar.gz"

    license("MIT")

    version("1.6.1", sha256="c93aaa500b439d71e4a5cf088d0006d2ce2c76f1950960c8843114e5f361dfd3")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", type=("build", "run"))
    depends_on("py-pytimeparse@1.1.5:", type=("build", "run"))
    depends_on("py-parsedatetime@2.1:", type=("build", "run"))
    depends_on("py-babel@2.0:", type=("build", "run"))
    depends_on("py-isodate@0.5.4:", type=("build", "run"))
    depends_on("py-python-slugify@1.2.1:", type=("build", "run"))
    depends_on("py-leather@0.3.2:", type=("build", "run"))
