# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestLazyFixture(PythonPackage):
    """It helps to use fixtures in pytest.mark.parametrize."""

    homepage = "https://github.com/tvorog/pytest-lazy-fixture"
    pypi = "pytest-lazy-fixture/pytest-lazy-fixture-0.6.3.tar.gz"

    license("MIT")

    version("0.6.3", sha256="0e7d0c7f74ba33e6e80905e9bfd81f9d15ef9a790de97993e34213deb5ad10ac")

    depends_on("py-setuptools", type="build")
    depends_on("py-pytest@3.2.5:", type=("build", "run"))
