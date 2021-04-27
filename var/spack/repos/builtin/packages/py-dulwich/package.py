# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyDulwich(PythonPackage):
    """Dulwich aims to provide an interface to Git repos
    (both local and remote) that doesn't call out to Git
    directory, but instead uses pure Python."""

    homepage = "https://www.dulwich.io"
    pypi     = "dulwich/dulwich-0.20.15.tar.gz"

    version('0.20.15', sha256='fb1773373ec2af896031f8312af6962a1b8b0176a2de3fb3d84a84ec04498888')
    version('0.20.14', sha256='21d6ee82708f7c67ce3fdcaf1f1407e524f7f4f7411a410a972faa2176baec0d')

    depends_on('python@3.5.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-certifi', type=('build', 'run'))
    depends_on('py-urllib3@1.24.1:', type=('build', 'run'))
