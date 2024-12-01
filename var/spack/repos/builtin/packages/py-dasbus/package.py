# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDasbus(PythonPackage):
    """Dasbus is a DBus library written in Python 3, based on GLib and inspired by pydbus."""

    homepage = "https://dasbus.readthedocs.io/en/latest/"
    pypi = "dasbus/dasbus-1.7.tar.gz"
    license("LGPL-2.1-or-later")

    version("1.7", sha256="a8850d841adfe8ee5f7bb9f82cf449ab9b4950dc0633897071718e0d0036b6f6")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pygobject", type=("build", "run"))
