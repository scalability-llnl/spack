# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFixtures(PythonPackage):
    """Fixtures, reusable state for writing clean tests and more."""

    homepage = "https://launchpad.net/python-fixtures"
    pypi = "fixtures/fixtures-3.0.0.tar.gz"

    license("Apache-2.0")

    version("3.0.0", sha256="fcf0d60234f1544da717a9738325812de1f42c2fa085e2d9252d8fff5712b2ef")

    depends_on("py-setuptools", type="build")
