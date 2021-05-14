# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyrsistent(PythonPackage):

    """Pyrsistent is a number of persistent collections
       (by some referred to as functional data structures).
       Persistent in the sense that they are immutable."""

    homepage = "http://github.com/tobgu/pyrsistent/"
    pypi = "pyrsistent/pyrsistent-0.15.7.tar.gz"

    version('0.16.0', sha256='28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3')
    version('0.15.7', sha256='cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))

    depends_on('py-tox')
    depends_on('py-sphinx')
    depends_on('py-sphinx-rtd-theme')
    depends_on('py-memory-profiler')
    depends_on('py-psutil')
    #depends_on('py-pyperform')
    depends_on('py-hypothesis')
