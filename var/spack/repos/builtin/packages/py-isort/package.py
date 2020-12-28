# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    url      = "https://pypi.io/packages/source/i/isort/isort-4.2.15.tar.gz"

    version('4.3.20', sha256='c40744b6bc5162bbb39c1257fe298b7a393861d50978b565f3ccd9cb9de0182a')
    version('4.2.15', sha256='79f46172d3a4e2e53e7016e663cc7a8b538bec525c36675fcfd2767df30b3983')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@4.3.0:')
    depends_on('py-futures', type=('build', 'run'), when='@4.3.0: ^python@:3.1')
    depends_on('py-backports-functools-lru-cache', type=('build', 'run'), when='@4.3.10: ^python@:3.1')
