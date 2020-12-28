# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsGit(PythonPackage):
    """Setuptools revision control system plugin for Git"""

    homepage = "https://pypi.python.org/pypi/setuptools-git"
    url      = "https://pypi.io/packages/source/s/setuptools-git/setuptools-git-1.2.tar.gz"

    version('1.2', sha256='ff64136da01aabba76ae88b050e7197918d8b2139ccbf6144e14d472b9c40445')

    depends_on('py-setuptools', type='build')
    depends_on('git')
