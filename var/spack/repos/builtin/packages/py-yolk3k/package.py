# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYolk3k(PythonPackage):
    """Yolk is a Python tool for obtaining information about installed Python
    packages and querying packages avilable on PyPI (Python Package Index).
    Yolk3k is a fork of the original yolk. `yolk3k` add Python 3 support and
    adds additional features."""

    homepage = "https://github.com/myint/yolk"
    pypi = "yolk3k/yolk3k-0.9.tar.gz"

    license("BSD-3-Clause")

    version("0.9", sha256="cf8731dd0a9f7ef50b5dc253fe0174383e3fed295a653672aa918c059eef86ae")

    depends_on("py-setuptools", type="build")
