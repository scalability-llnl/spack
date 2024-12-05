# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChronyk(PythonPackage):
    """A small Python 3 library containing some handy tools for handling time,
    especially when it comes to interfacing with those pesky humans."""

    homepage = "https://github.com/KoffeinFlummi/Chronyk/"
    url = "https://github.com/KoffeinFlummi/Chronyk/archive/v1.0.1.tar.gz"

    license("MIT")

    version("1.0.1", sha256="fc47773ab27d68b56f241ff112b72c2b6590558769b3f225994175ca75115bc8")
    version("0.9.1", sha256="94ebef9f8cf282136413b3963a958b2ab8aad3d552987b56afb3d517cd1e3e59")

    depends_on("py-setuptools", type="build")
    depends_on("python@3:", type=("build", "run"))
