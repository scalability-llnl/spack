# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyreadline(PythonPackage):
    """A Python implementation of GNU readline functionality."""

    homepage = "https://github.com/pyreadline/pyreadline"
    git = "https://github.com/pyreadline/pyreadline.git"
    pypi = "pyreadline/pyreadline-2.1.zip"

    version("master", branch="master")
    version("2.1", sha256="4530592fc2e85b25b1a9f79664433da09237c1a270e4d78ea5aa3a2c7229e2d1")

    depends_on("py-setuptools", type="build")
