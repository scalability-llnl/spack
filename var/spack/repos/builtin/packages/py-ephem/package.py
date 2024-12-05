# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEphem(PythonPackage):
    """PyEphem provides an ephem Python package for
    performing high-precision astronomy computations."""

    homepage = "https://rhodesmill.org/pyephem/"
    url = "https://github.com/brandon-rhodes/pyephem/archive/v3.7.7.1.tar.gz"

    license("MIT")

    version("3.7.7.1", sha256="d9d05d85c0d38a79169acaef25964ac9df2d808f0d833354545b9ef681ff584d")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
