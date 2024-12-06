# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyLruDict(PythonPackage):
    """A fast LRU cache"""

    homepage = "https://github.com/amitdev/lru-dict"
    pypi = "lru-dict/lru-dict-1.1.6.tar.gz"

    license("MIT")

    version("1.1.6", sha256="365457660e3d05b76f1aba3e0f7fedbfcd6528e97c5115a351ddd0db488354cc")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
