# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGitdb(PythonPackage):
    """The GitDB project implements interfaces to allow read and write access
    to git repositories."""

    homepage = "https://gitdb.readthedocs.io"
    url      = "https://pypi.io/packages/source/g/gitdb/gitdb-4.0.5.tar.gz"

    version('4.0.5', sha256='c9e1f2d0db7ddb9a704c2a0217be31214e91a4fe1dea1efad19ae42ba0c285c9')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-smmap@3.0.1:3.999', type=('build', 'run'))
