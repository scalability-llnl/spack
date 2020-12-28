# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyStdlibList(PythonPackage):
    """This package includes lists of all of the standard libraries
    for Python, along with the code for scraping the official Python
    docs to get said lists."""

    homepage = "https://pypi.python.org/project/stdlib-list"
    url      = "https://pypi.io/packages/source/s/stdlib-list/stdlib-list-0.6.0.tar.gz"

    version('0.6.0', sha256='133cc99104f5a4e1604dc88ebb393529bd4c2b99ae7e10d46c0b596f3c67c3f0')

    depends_on('py-functools32', when="^python@:3.1", type=('build', 'run'))
    depends_on('py-setuptools', type='build')
