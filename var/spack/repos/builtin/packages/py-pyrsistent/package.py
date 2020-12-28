# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrsistent(PythonPackage):
    """Pyrsistent is a number of persistent collections
       (by some referred to as functional data structures).
       Persistent in the sense that they are immutable."""

    homepage = "http://github.com/tobgu/pyrsistent/"
    url      = "https://pypi.io/packages/source/p/pyrsistent/pyrsistent-0.15.7.tar.gz"

    version('0.15.7', sha256='cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
