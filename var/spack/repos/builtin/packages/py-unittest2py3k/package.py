# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUnittest2py3k(PythonPackage):
    """unittest2 is a backport of the new features added to the unittest
    testing framework in Python 2.7 and 3.2. This is a Python 3 compatible
    version of unittest2."""

    pypi = "unittest2py3k/unittest2py3k-0.5.1.tar.gz"

    version("0.5.1", sha256="78249c5f1ac508a34d9d131d43a89d77bf154186f3ea5f7a6b993d3f3535d403")

    depends_on("python@3:")
    depends_on("py-setuptools", type="build")
