# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/rtfd/sphinx_rtd_theme/"
    url      = "https://github.com/readthedocs/sphinx_rtd_theme/archive/0.5.0.tar.gz"

    version('0.5.0',        sha256='f5c77e9026e2bd0b3d2530f9f8a6681808b216ba70195fe56e7ad89f641ac447')
    version('0.4.3',        sha256='3412195caad06e4537ad741596d57706c3ed29073d1e0e6b46f25e344d0f393b')
    version('0.2.5b1',      sha256='31924cdaa5232d1d573423ebebeb1e8f02c8b3cd8cd0662b8a91f3b12efbc12e')
    version('0.1.10-alpha', sha256='a4c120c0d5c87a2541da9d5e48d3c43b96ea7d7867eacbd5dbf125cdeaa0b4f0')

    depends_on('py-setuptools', type='build')
    depends_on('npm', when='@0.5.0:', type='build')
    depends_on('py-sphinx', when='@0.4.1:', type=('build', 'run'))
