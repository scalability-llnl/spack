# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymsgbox(PythonPackage):
    """A simple, cross-platform, pure Python module for
    JavaScript-like message boxes."""

    homepage = "https://github.com/asweigart/pymsgbox"
    pypi = "PyMsgBox/PyMsgBox-1.0.9.tar.gz"

    version("1.0.9", sha256="2194227de8bff7a3d6da541848705a155dcbb2a06ee120d9f280a1d7f51263ff")

    depends_on("py-setuptools", type="build")
