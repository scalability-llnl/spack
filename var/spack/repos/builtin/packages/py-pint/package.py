# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPint(PythonPackage):
    """Pint is a Python package to define, operate and manipulate physical
    quantities: the product of a numerical value and a unit of measurement.
    It allows arithmetic operations between them and conversions from and
    to different units."""

    homepage = "https://pypi.org/project/Pint"
    url = "https://pypi.io/packages/source/p/pint/Pint-0.11.tar.gz"

    version('0.11', sha256='308f1070500e102f83b6adfca6db53debfce2ffc5d3cbe3f6c367da359b5cf4d')
    version('0.10.1', sha256='d739c364b8326fe3d70773d5720fa8b005ea6158695cad042677a588480c86e6')
    version('0.10', sha256='38a4d6e242b8bab693cd83a5f5ade3d816463b498658e7ab14ce64c4d458c88b')
    version('0.9', sha256='32d8a9a9d63f4f81194c0014b3b742679dce81a26d45127d9810a68a561fe4e2')
    version('0.8.1', sha256='afcf31443a478c32bbac4b00337ee9026a13d0e2ac83d30c79151462513bb0d4')

    depends_on('python@3.6:', type=('build', 'run'), when='@0.10:')
    depends_on('py-setuptools', type=('build', ))
    depends_on('py-setuptools-scm', type=('build', ))
