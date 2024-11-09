# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy2bit(PythonPackage):
    """A package for accessing 2bit files using lib2bit."""

    pypi = "py2bit/py2bit-0.2.1.tar.gz"

    license("MIT")

    version("0.2.1", sha256="34f7ac22be0eb4b5493063826bcc2016a78eb216bb7130890b50f3572926aeb1")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
