# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNodeSemver(PythonPackage):
    """python version of node-semver (https://github.com/isaacs/node-semver)"""

    homepage = "https://github.com/podhmo/python-semver"
    pypi = "node-semver/node-semver-0.8.1.tar.gz"

    license("MIT")

    version("0.8.1", sha256="281600d009606f4f63ddcbe148992e235b39a69937b9c20359e2f4a2adbb1e00")
    version("0.6.1", sha256="4016f7c1071b0493f18db69ea02d3763e98a633606d7c7beca811e53b5ac66b7")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
