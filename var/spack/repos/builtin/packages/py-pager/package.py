# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPager(PythonPackage):
    """Python module that pages output to the screen,
    reads keys and console dimensions without executing external utils."""

    pypi = "pager/pager-3.3.tar.gz"

    license("MIT")

    version("3.3", sha256="18aa45ec877dca732e599531c7b3b0b22ed6a4445febdf1bdf7da2761cca340d")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
