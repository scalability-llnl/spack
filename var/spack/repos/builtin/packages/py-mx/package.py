# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMx(PythonPackage):
    """The eGenix.com mx Base Distribution for Python is a collection of
    professional quality software tools which enhance Python's
    usability in many important areas such as fast text searching,
    date/time processing and high speed data types.

    """

    homepage = "https://www.egenix.com/products/python/mxBase/"
    url = "https://downloads.egenix.com/python/egenix-mx-base-3.2.8.tar.gz"

    license("eGenix")

    version("3.2.8", sha256="0da55233e45bc3f88870e62e60a79c2c86bad4098b8128343fd7be877f44a3c0")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
