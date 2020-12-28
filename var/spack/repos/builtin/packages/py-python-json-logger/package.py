# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonJsonLogger(PythonPackage):
    """"A python library adding a json log formatter."""

    homepage = "https://github.com/madzak/python-json-logger"
    url      = "https://pypi.io/packages/source/p/python-json-logger/python-json-logger-0.1.11.tar.gz"

    version('0.1.11', sha256='b7a31162f2a01965a5efb94453ce69230ed208468b0bbc7fdfc56e6d8df2e281')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools')
