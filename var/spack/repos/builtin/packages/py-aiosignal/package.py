# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAiosignal(PythonPackage):
    """A project to manage callbacks in asyncio projects."""

    homepage = "https://aiosignal.readthedocs.io/"
    pypi = "aiosignal/aiosignal-1.2.0.tar.gz"

    license("Apache-2.0")

    version("1.2.0", sha256="78ed67db6c7b7ced4f98e495e572106d5c432a93e1ddd1bf475e1dc05f5b7df2")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-frozenlist@1.1.0:", type=("build", "run"))
