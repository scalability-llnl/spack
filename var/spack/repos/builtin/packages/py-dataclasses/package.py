# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyDataclasses(PythonPackage):
    """A backport of the dataclasses module for Python 3.6"""

    homepage = "https://github.com/ericvsmith/dataclasses"
    pypi = "dataclasses/dataclasses-0.7.tar.gz"

    version('0.7', sha256='494a6dcae3b8bcf80848eea2ef64c0cc5cd307ffc263e17cdf42f3e5420808e6')

    depends_on('python@3.6.00:3.6.99', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
