# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyGooglePasta(PythonPackage):
    """pasta is an AST-based Python refactoring library."""

    homepage = "https://github.com/google/pasta"
    pypi = "google-pasta/google-pasta-0.1.8.tar.gz"

    version('0.2.0', sha256='c9f2c8dfc8f96d0d5808299920721be30c9eec37f2389f28904f454565c8a16e')
    version('0.1.8', sha256='713813a9f7d6589e5defdaf21e80e4392eb124662f8bd829acd51a4f8735c0cb')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
