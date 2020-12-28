# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyXattr(PythonPackage):
    """A python interface to access extended file attributes,
    sans libattr dependency.
    """

    homepage = "http://pyxattr.k1024.org/"
    url = "https://pypi.io/packages/source/x/xattr/xattr-0.9.6.tar.gz"
    git = "https://github.com/iustin/pyxattr.git"

    version('master', branch='master')
    version('0.9.6', sha256='7cb1b28eeab4fe99cc4350e831434142fce658f7d03f173ff7722144e6a47458')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
