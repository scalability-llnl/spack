# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyeda(PythonPackage):
    """PyEDA is a Python library for electronic design automation."""

    homepage = "https://github.com/cjdrake/pyeda"
    pypi = "pyeda/pyeda-0.28.0.tar.gz"

    license("BSD-2-Clause")

    version("0.28.0", sha256="07185f458d5d0b2ba5058da8b95dad6ab7684ceaf41237a25bcd3f005490f59d")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("python@3.3:", type=("build", "run"))
