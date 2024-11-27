# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJdatetime(PythonPackage):
    """jdatetime is Jalali implementation of Python's datetime module"""

    homepage = "https://github.com/slashmili/python-jalali"
    pypi = "jdatetime/jdatetime-3.6.2.tar.gz"

    version("3.6.2", sha256="a589e35f0dab89283c1a3de9d70ed6cf657932aaed8e8ce1b0e5801aaab1da67")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
