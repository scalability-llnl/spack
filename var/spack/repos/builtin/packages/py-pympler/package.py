# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
        of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    url      = "https://pypi.io/packages/source/P/Pympler/Pympler-0.4.3.tar.gz"

    version('0.4.3', sha256='430528fff6cde1bae0a305e8df647b158c3cc4930cff122bf228293829ee1e56')
    version('0.4.2', sha256='3c3f9d8eb3dddf4f29c433433ea77c9c3f2f0dcc06575c0c2a9d81b2602893b2')
    version('0.4.1', sha256='6a8bfd2972c4ec34ac8750358515950be4a4ca13dfa6a05a9a22419786745f90')
    version('0.4',   sha256='b280480502df658b18cb6310d2c744fabf05d4c518f873377884b4d4b5d2992d')
    version('0.3.1', sha256='8cb170fddfe592342856590e2239e8c20ac61eacf18bc4f65a95ccaf74475e3e')

    depends_on('python@2.5:')
