# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPep8(PythonPackage):
    """Python style guide checker (deprecated, use py-pycodestyle instead)."""

    homepage = "https://pep8.readthedocs.org/"
    pypi = "pep8/pep8-1.7.1.tar.gz"

    version("1.7.1", sha256="fe249b52e20498e59e0b5c5256aa52ee99fc295b26ec9eaa85776ffdb9fe6374")

    depends_on("py-setuptools", type=("build", "run"))
