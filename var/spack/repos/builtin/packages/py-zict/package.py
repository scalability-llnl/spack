# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZict(PythonPackage):
    """Mutable mapping tools"""

    homepage = "https://zict.readthedocs.io/en/latest/"
    pypi = "zict/zict-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version("3.0.0", sha256="e321e263b6a97aafc0790c3cfb3c04656b7066e6738c37fffcca95d803c9fba5")
    version("1.0.0", sha256="e34dd25ea97def518fb4c77f2c27078f3a7d6c965b0a3ac8fe5bdb0a8011a310")

    depends_on("python@3.8:", when="@3.0.0:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-heapdict", type=("build", "run"), when="@:2.2.0")
