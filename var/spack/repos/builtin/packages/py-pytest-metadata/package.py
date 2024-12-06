# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestMetadata(PythonPackage):
    """pytest plugin for test session metadata"""

    homepage = "https://github.com/pytest-dev/pytest-metadata"
    pypi = "pytest-metadata/pytest-metadata-1.11.0.tar.gz"

    version("1.11.0", sha256="71b506d49d34e539cc3cfdb7ce2c5f072bea5c953320002c95968e0238f8ecf1")

    depends_on("python@2.7:2.8,3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-pytest@2.9:", type=("build", "run"))
