# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygit2(PythonPackage):
    """Pygit2 is a set of Python bindings to the libgit2 shared library,
    libgit2 implements the core of Git.
    """

    homepage = "http://www.pygit2.org/"
    url      = "https://pypi.io/packages/source/p/pygit2/pygit2-0.24.1.tar.gz"

    version('0.24.1', sha256='4d1d0196b38d6012faf0a7c45e235c208315672b6035da504566c605ba494064')

    extends('python')
    depends_on('py-setuptools', type='build')
    # Version must match with libgit2
    # See: http://www.pygit2.org/install.html
    depends_on('libgit2@0.24:', when='@0.24:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))

    def setup_build_environment(self, env):
        spec = self.spec
        # http://www.pygit2.org/install.html
        env.set('LIBGIT2', spec['libgit2'].prefix)
        env.set('LIBGIT2_LIB', spec['libgit2'].prefix.lib)
