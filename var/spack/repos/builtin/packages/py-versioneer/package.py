# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/warner/python-versioneer"
    url      = "https://github.com/warner/python-versioneer/archive/0.18.tar.gz"
    git      = "https://github.com/warner/python-versioneer.git"

    maintainers = ['scemama']

    version('0.18', sha256='cf895b67f5bc62d61c4837458069ded8f66b4e5764c19f7253c51ee27e8b3a99')

    depends_on('py-setuptools', type='build')
