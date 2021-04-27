# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyJeepney(PythonPackage):
    """Low-level, pure Python DBus protocol wrapper."""

    homepage = "https://gitlab.com/takluyver/jeepney"
    pypi = "jeepney/jeepney-0.4.3.tar.gz"

    version('0.4.3', sha256='3479b861cc2b6407de5188695fa1a8d57e5072d7059322469b62628869b8e36e')

    depends_on('python@3.5:', type=('build', 'run'))
