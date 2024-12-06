# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

from spack.package import *


class PySphinxcontribJsmath(PythonPackage):
    """A sphinx extension which renders display math in HTML via JavaScript."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-jsmath/sphinxcontrib-jsmath-1.0.1.tar.gz"

    # 'sphinx' requires 'sphinxcontrib-jsmath' at build-time, but
    # 'sphinxcontrib-jsmath' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules: List[str] = []

    license("BSD-2-Clause")

    version("1.0.1", sha256="a9925e4a4587247ed2191a22df5f6970656cb8ca2bd6284309578f2153e0c4b8")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
