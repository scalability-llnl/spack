# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestAstropyHeader(PythonPackage):
    """pytest plugin to add diagnostic information to the header of the test output."""

    homepage = "https://github.com/astropy/pytest-astropy-header"
    pypi = "pytest-astropy-header/pytest-astropy-header-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version("0.2.2", sha256="77891101c94b75a8ca305453b879b318ab6001b370df02be2c0b6d1bb322db10")

    depends_on("py-setuptools@30.3.0:", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-pytest@4.6:", type=("build", "run"))
