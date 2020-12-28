# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReadmeRenderer(PythonPackage):
    """readme_renderer is a library for rendering "readme" descriptions
    for Warehouse."""

    homepage = "https://github.com/pypa/readme_renderer"
    url      = "https://pypi.io/packages/source/r/readme_renderer/readme_renderer-24.0.tar.gz"

    version('24.0', sha256='bb16f55b259f27f75f640acf5e00cf897845a8b3e4731b5c1a436e4b8529202f')
    version('16.0', sha256='c46b3418ddef3c3c3f819a4a9cfd56ede15c03d12197962a7e7a89edf1823dd5')

    depends_on('py-setuptools', type='build')
    depends_on('py-bleach@2.1.0:', type=('build', 'run'))
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
