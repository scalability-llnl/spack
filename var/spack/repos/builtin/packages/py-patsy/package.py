# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPatsy(PythonPackage):
    """A Python package for describing statistical models and for
    building design matrices."""

    homepage = "https://github.com/pydata/patsy"
    url      = "https://pypi.io/packages/source/p/patsy/patsy-0.4.1.zip"

    version('0.5.1', sha256='f115cec4201e1465cd58b9866b0b0e7b941caafec129869057405bfe5b5e3991',
            url="https://pypi.io/packages/source/p/patsy/patsy-0.5.1.tar.gz")
    version('0.4.1', sha256='dc1cc280045b0e6e50c04706fd1e26d2a00ea400aa112f88e8142f88b0b7d3d4')

    variant('splines', default=False, description="Offers spline related functions")

    depends_on('py-setuptools',  type='build')
    depends_on('py-numpy',       type=('build', 'run'))
    depends_on('py-scipy',       type=('build', 'run'), when="+splines")
    depends_on('py-six',         type=('build', 'run'))
