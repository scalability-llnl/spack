# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGooglePasta(PythonPackage):
    """pasta is an AST-based Python refactoring library."""

    homepage = "https://github.com/google/pasta"
    url      = "https://pypi.io/packages/source/g/google-pasta/google-pasta-0.1.8.tar.gz"

    version('0.1.8', sha256='713813a9f7d6589e5defdaf21e80e4392eb124662f8bd829acd51a4f8735c0cb')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
