# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJamo(PythonPackage):
    """Python-jamo is a Python Hangul syllable decomposition
    and synthesis library for working with Hangul characters
    and jamo."""

    homepage = "https://github.com/jdongian/python-jamo"
    pypi = "jamo/jamo-0.4.1.tar.gz"

    license("Apache-2.0")

    version("0.4.1", sha256="ea65cf9d35338d0e0af48d75ff426d8a369b0ebde6f07051c3ac37256f56d025")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
