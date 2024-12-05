# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCalver(PythonPackage):
    """The calver package is a setuptools extension for automatically
    defining your Python package version as a calendar version."""

    homepage = "https://github.com/di/calver"
    pypi = "calver/calver-2022.6.26.tar.gz"

    license("Apache-2.0")

    version("2022.6.26", sha256="e05493a3b17517ef1748fbe610da11f10485faa7c416b9d33fd4a52d74894f8b")

    depends_on("py-setuptools", type="build")
