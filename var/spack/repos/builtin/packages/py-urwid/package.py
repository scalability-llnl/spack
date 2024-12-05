# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrwid(PythonPackage):
    """A full-featured console UI library"""

    homepage = "https://urwid.org/"
    pypi = "urwid/urwid-1.3.0.tar.gz"

    license("LGPL-2.1-only")

    version("2.1.2", sha256="588bee9c1cb208d0906a9f73c613d2bd32c3ed3702012f51efe318a3f2127eae")
    version("1.3.0", sha256="29f04fad3bf0a79c5491f7ebec2d50fa086e9d16359896c9204c6a92bc07aba2")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
