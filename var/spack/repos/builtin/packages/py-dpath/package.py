# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyDpath(PythonPackage):
    """A python library for accessing and searching dictionaries via
       /slashed/paths ala xpath."""

    homepage = "https://github.com/akesterson/dpath-python"
    pypi     = "dpath/dpath-2.0.1.tar.gz"

    version('2.0.1', sha256='bea06b5f4ff620a28dfc9848cf4d6b2bfeed34238edeb8ebe815c433b54eb1fa')

    depends_on('python@2.7:', type=('build', 'run'))
