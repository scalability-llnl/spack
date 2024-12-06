# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Py3to2(PythonPackage):
    """lib3to2 is a set of fixers that are intended to backport code written
    for Python version 3.x into Python version 2.x."""

    pypi = "3to2/3to2-1.1.1.zip"

    version("1.1.1", sha256="fef50b2b881ef743f269946e1090b77567b71bb9a9ce64b7f8e699b562ff685c")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
