# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PySphinxcontribBibtex(PythonPackage):
    """A Sphinx extension for BibTeX style citations."""

    pypi = "sphinxcontrib-bibtex/sphinxcontrib-bibtex-0.3.5.tar.gz"

    version('2.0.0', sha256='98e18eb0b088d3f556199f3fbb91d3d48ebb7596fe86b6c37cc4c4dc5419b7a1')
    version('1.0.0', sha256='629612b001f86784669d65e662377a482052decfd9a0a17c46860878eef7b9e0')
    version('0.3.5', sha256='c93e2b4a0d14f0ab726f95f0a33c1675965e9df3ed04839635577b8f978206cd')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'), when='@1:')
    depends_on('python@3.6:', type=('build', 'run'), when='@2:')
    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@0.3.0:', type=('build', 'run'))
    depends_on('py-pybtex@0.17:', type=('build', 'run'), when='@:1.9.9')
    depends_on('py-pybtex@0.20:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-pybtex-docutils@0.2.0:', type=('build', 'run'), when='@:1.9.9')
    depends_on('py-pybtex-docutils@0.2.2:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-six@1.4.1:', type=('build', 'run'), when='@0.3.5')
    depends_on('py-sphinx@1.0:', type=('build', 'run'), when='@:1.9.9')
    depends_on('py-sphinx@2.0:', type=('build', 'run'), when='@2.0.0:')
    depends_on('py-oset@0.1.3:', type=('build', 'run'))
    depends_on('py-ordereddict@1.1:', when='^python@:2.6', type=('build', 'run'))
