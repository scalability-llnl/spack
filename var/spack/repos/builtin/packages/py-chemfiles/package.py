# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChemfiles(PythonPackage):
    """Python interface to chemfiles"""

    homepage = "http://chemfiles.org/chemfiles.py/latest/"
    pypi = "chemfiles/chemfiles-0.10.3.tar.gz"

    maintainers("RMeli")

    license("BSD-3-Clause")

    version("0.10.3", sha256="4bbb8b116492a57dbf6ddb4c84aad0133cd782e0cc0e53e4b957f2d93e6806ea")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("chemfiles@0.10.3+shared", when="@0.10.3")

    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-setuptools@44:", type="build")
    depends_on("py-wheel@0.36:", type="build")
    depends_on("cmake", type="build")
    depends_on("ninja", type="build")
