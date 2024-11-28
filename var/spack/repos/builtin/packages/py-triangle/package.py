# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTriangle(PythonPackage):
    """Python bindings to the triangle library"""

    homepage = "https://github.com/drufat/triangle"
    pypi = "triangle/triangle-20200424.tar.gz"

    license("LGPL-3.0")

    version("20200424", sha256="fc207641f8f39986f7d2bee1b91688a588cd235d2e67777422f94e61fece27e9")

    depends_on("c", type="build")  # generated

    depends_on("python@:3.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")

    depends_on("triangle", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
