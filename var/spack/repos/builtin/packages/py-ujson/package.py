# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUjson(PythonPackage):
    """Ultra fast JSON decoder and encoder written in C with Python
       bindings."""

    homepage = "https://github.com/esnme/ultrajson"
    pypi = "ujson/ujson-1.35.tar.gz"

    version('4.0.2', sha256='c615a9e9e378a7383b756b7e7a73c38b22aeb8967a8bfbffd4741f7ffd043c4d')
    version('1.35', sha256='f66073e5506e91d204ab0c614a148d5aa938bdbf104751be66f8ad7a222f5f86')

    depends_on('python@3.6:', type=('build', 'run'), when='@4:')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build', when='@4:')
