# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonRapidjson(PythonPackage):
    """Python wrapper around rapidjson."""

    homepage = "https://github.com/python-rapidjson/python-rapidjson"
    url      = "https://pypi.io/packages/source/p/python-rapidjson/python-rapidjson-0.9.1.tar.gz"

    version('0.9.1', sha256='ad80bd7e4bb15d9705227630037a433e2e2a7982b54b51de2ebabdd1611394a1')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
