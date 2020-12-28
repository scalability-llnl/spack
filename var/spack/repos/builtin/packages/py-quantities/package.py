# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQuantities(PythonPackage):
    """Support for physical quantities with units, based on numpy"""

    homepage = "http://python-quantities.readthedocs.org"
    url      = "https://pypi.io/packages/source/q/quantities/quantities-0.12.1.tar.gz"

    version('0.12.1', sha256='0a03e8511db603c57ca80dee851c43f08d0457f4d592bcac2e154570756cb934')
    version('0.11.1', sha256='4382098a501b55bf0fdb3dba2061a161041253697d78811ecfd7c55449836660',
            url="https://pypi.io/packages/source/q/quantities/quantities-0.11.1.zip")

    conflicts('^py-numpy@1.13:', when='@:0.11.99')

    depends_on('python@2.6.0:')
    depends_on('py-numpy@1.4.0:', type=('build', 'run'))
