# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlosc(PythonPackage):
    """A Python wrapper for the extremely fast Blosc compression library"""

    homepage = "http://python-blosc.blosc.org"
    url = "https://github.com/Blosc/python-blosc/archive/v1.9.1.tar.gz"
    git = "https://github.com/Blosc/python-blosc.git"

    license("BSD-3-Clause")

    version("1.9.1", sha256="ffc884439a12409aa4e8945e21dc920d6bc21807357c51d24c7f0a27ae4f79b9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("cmake@3.11:", type="build")
    depends_on("ninja", type="build")
    # depends_on('c-blosc')  # shipped internally
