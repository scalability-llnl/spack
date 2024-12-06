# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPython3Xlib(PythonPackage):
    """python3-xlib is python3 version of python-xlib."""

    pypi = "python3-xlib/python3-xlib-0.15.tar.gz"

    version("0.15", sha256="dc4245f3ae4aa5949c1d112ee4723901ade37a96721ba9645f2bfa56e5b383f8")

    depends_on("python@3:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
