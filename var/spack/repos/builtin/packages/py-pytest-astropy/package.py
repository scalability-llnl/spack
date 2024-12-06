# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAstropy(PythonPackage):
    """Meta-package containing dependencies for testing."""

    homepage = "https://github.com/astropy/pytest-astropy"
    pypi = "pytest-astropy/pytest-astropy-0.10.0.tar.gz"

    license("BSD-3-Clause")

    version("0.10.0", sha256="85e3c66ceede4ce668f473b3cf377fcb2aa3c48e24f28aaa377ae86004cce211")

    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-pytest@4.6:", type=("build", "run"))
    depends_on("py-pytest-doctestplus@0.11:", type=("build", "run"))
    depends_on("py-pytest-remotedata@0.3.1:", type=("build", "run"))
    depends_on("py-pytest-openfiles@0.3.1:", type=("build", "run"))
    depends_on("py-pytest-astropy-header@0.1.2:", type=("build", "run"))
    depends_on("py-pytest-arraydiff@0.1:", type=("build", "run"))
    depends_on("py-pytest-filter-subpackage@0.1:", type=("build", "run"))
    depends_on("py-pytest-cov@2.3.1:", type=("build", "run"))
    depends_on("py-pytest-mock@2:", type=("build", "run"))
    depends_on("py-attrs@19.2:", type=("build", "run"))
    depends_on("py-hypothesis@5.1:", type=("build", "run"))
