# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyenchant(PythonPackage):
    """Sphinx Documentation Generator."""

    homepage = "https://pyenchant.github.io/pyenchant/"
    pypi = "pyenchant/pyenchant-3.2.2.tar.gz"
    git = "https://github.com/pyenchant/pyenchant.git"

    license("LGPL-2.1")

    version("3.2.2", sha256="1cf830c6614362a78aab78d50eaf7c6c93831369c52e1bb64ffae1df0341e637")

    depends_on("enchant")
    depends_on("python@3.5:")
    depends_on("py-setuptools")
