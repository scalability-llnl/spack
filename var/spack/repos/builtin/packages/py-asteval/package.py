# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsteval(PythonPackage):
    """Safe, minimalistic evaluator of python expression using ast module"""

    homepage = "http://github.com/newville/asteval"
    url      = "https://pypi.io/packages/source/a/asteval/asteval-0.9.18.tar.gz"

    version('0.9.18', sha256='5d64e18b8a72c2c7ae8f9b70d1f80b68bbcaa98c1c0d7047c35489d03209bc86')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
