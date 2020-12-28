# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAstor(PythonPackage):
    """
    astor is designed to allow easy manipulation of Python source via the AST.
    """

    homepage = "https://pypi.python.org/pypi/astor"
    url      = "https://pypi.io/packages/source/a/astor/astor-0.8.0.tar.gz"

    version('0.8.0', sha256='37a6eed8b371f1228db08234ed7f6cfdc7817a3ed3824797e20cbb11dc2a7862')
    version('0.6',   sha256='175ec395cde36aa0178c5a3120d03954c65d1ef4bb19ec4aa30e9d7a7cc426c4')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # Build fails with newer versions of setuptools
    # https://github.com/berkerpeksag/astor/issues/162
    # https://github.com/berkerpeksag/astor/pull/163
    patch('https://github.com/berkerpeksag/astor/pull/163/commits/30059dac4eb832e58ab2109db84508b294ba366d.patch',
          sha256='edc5eeddabe153b08e938f52edaeb2d880ee3128082967f310db0f98510fe6e0',
          when='@0.8.0')
