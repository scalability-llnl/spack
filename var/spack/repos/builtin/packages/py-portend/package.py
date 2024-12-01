# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPortend(PythonPackage):
    """TCP port monitoring and discovery"""

    homepage = "https://github.com/jaraco/portend"
    pypi = "portend/portend-2.5.tar.gz"

    license("MIT")

    version("2.5", sha256="19dc27bfb3c72471bd30a235a4d5fbefef8a7e31cab367744b5d87a205e7bfd9")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm@1.15.0:", type="build")
    depends_on("py-tempora@1.8:", type=("run", "build"))
    depends_on("python@2.7:", type=("run", "build"))
