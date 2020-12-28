# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIdentify(PythonPackage):
    """File identification library for Python.

    Given a file (or some information about a file), return a set of
    standardized tags identifying what the file is."""

    homepage = "https://github.com/chriskuehl/identify"
    url      = "https://pypi.io/packages/source/i/identify/identify-1.4.7.tar.gz"

    version('1.4.7', sha256='d8919589bd2a5f99c66302fec0ef9027b12ae150b0b0213999ad3f695fc7296e')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
