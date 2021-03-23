# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyAioitertools(PythonPackage):
    """Implementation of itertools, builtins, and more for AsyncIO and mixed-type
    iterables."""

    homepage = "https://aioitertools.omnilib.dev/en/stable/"
    pypi     = "aioitertools/aioitertools-0.7.1.tar.gz"

    version('0.7.1', sha256='54a56c7cf3b5290d1cb5e8974353c9f52c677612b5d69a859369a020c53414a3')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7:', type=('build', 'run'))
