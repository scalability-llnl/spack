# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCattrs(PythonPackage):
    """An open source Python library for structuring and unstructuring data."""

    homepage = "https://github.com/python-attrs/cattrs"
    pypi = "cattrs/cattrs-22.2.0.tar.gz"

    license("MIT")

    version("22.2.0", sha256="f0eed5642399423cf656e7b66ce92cdc5b963ecafd041d1b24d136fdde7acf6d")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-poetry-core@1.1.0:", type="build")

    depends_on("py-attrs@20:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
    depends_on("py-exceptiongroup", when="^python@:3.10", type=("build", "run"))
