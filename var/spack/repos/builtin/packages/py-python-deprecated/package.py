# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonDeprecated(PythonPackage):
    """Python @deprecated decorator to deprecate old python classes, functions or methods."""

    homepage = "https://github.com/vrcmarcos/python-deprecated"
    pypi = "Python-Deprecated/Python-Deprecated-1.1.0.tar.gz"

    maintainers("Pandapip1")

    version("1.1.0", sha256="a242b3c1721f97912330b12cd5529abfa5b3876084a6c60a2c683a87d4b0dd6f")

    depends_on("py-setuptools", type=("build",))
