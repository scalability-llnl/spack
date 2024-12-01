# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsMock(PythonPackage):
    """Mock out responses from the requests package."""

    homepage = "https://requests-mock.readthedocs.io/"
    pypi = "requests-mock/requests-mock-1.7.0.tar.gz"

    version("1.7.0", sha256="88d3402dd8b3c69a9e4f9d3a73ad11b15920c6efd36bc27bf1f701cf4a8e4646")

    depends_on("py-setuptools", type="build")
