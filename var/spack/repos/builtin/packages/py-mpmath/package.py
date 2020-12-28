# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpmath(PythonPackage):
    """A Python library for arbitrary-precision floating-point arithmetic."""
    homepage = "http://mpmath.org"
    url      = "https://pypi.io/packages/source/m/mpmath/mpmath-1.0.0.tar.gz"

    version('1.1.0', sha256='fc17abe05fbab3382b61a123c398508183406fa132e0223874578e20946499f6')
    version('1.0.0', sha256='04d14803b6875fe6d69e6dccea87d5ae5599802e4b1df7997bddd2024001050c')
    version('0.19', sha256='68ddf6426dcda445323467d89892d2cffbbd1ae0b31ac1241b1b671749d63222')
