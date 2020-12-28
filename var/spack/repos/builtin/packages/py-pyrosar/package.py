# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyrosar(PythonPackage):
    """A framework for large-scale SAR satellite data processing"""

    homepage = "https://github.com/johntruckenbrodt/pyroSAR"
    url      = "https://github.com/johntruckenbrodt/pyroSAR/archive/v0.8.tar.gz"

    version('0.8', sha256='03f6d846afde85807a63f84b1fd25fe61e9a4cda93e9af7d44a67fd4b0b7dbc8')

    # python
    depends_on('py-setuptools', type='build')
    depends_on('py-progressbar2', type=('build', 'run'))
    depends_on('py-pathos@0.2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.16.3', type=('build', 'run'))
    depends_on('py-scoop', type=('build', 'run'))
    depends_on('py-spatialist@0.2.8', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    # other
    depends_on('gdal+python', type=('build', 'link', 'run'))
