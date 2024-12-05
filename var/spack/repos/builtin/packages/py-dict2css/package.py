# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDict2css(PythonPackage):
    """A μ-library for constructing cascading style sheets from Python dictionaries."""

    homepage = "https://github.com/sphinx-toolbox/dict2css"
    pypi = "dict2css/dict2css-0.3.0.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version("0.3.0", sha256="1e8b1bf580dca2083198f88a60ec88c878a8829d760dfe45483ef80fe2905117")

    depends_on("py-whey", type="build")
    depends_on("py-cssutils@2.2.0:", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.2.0:", type=("build", "run"))
