# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGeopandas(PythonPackage):
    """GeoPandas is an open source project to make working with geospatial
       data in python easier. GeoPandas extends the datatypes used by pandas
       to allow spatial operations on geometric types. Geometric operations are
       performed by shapely. Geopandas further depends on fiona for file access
       and descartes and matplotlib for plotting."""

    homepage = "https://geopandas.org/"
    pypi = "geopandas/geopandas-0.8.1.tar.gz"
    git      = "https://github.com/geopandas/geopandas.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('0.9.0', sha256='63972ab4dc44c4029f340600dcb83264eb8132dd22b104da0b654bef7f42630a')
    version('0.8.2', sha256='aa9ae82e4e6b52efa244bd4b8bd2363d66693e5592ad1a0f52b6afa8c36348cb')
    version('0.8.1', sha256='e28a729e44ac53c1891b54b1aca60e3bc0bb9e88ad0f2be8e301a03b9510f6e2')
    version('0.5.0', sha256='d075d2ab61a502ab92ec6b72aaf9610a1340ec24ed07264fcbdbe944b9e68954')
    version('0.4.0', sha256='9f5d24d23f33e6d3267a633025e4d9e050b3a1e86d41a96d3ccc5ad95afec3db')
    version('0.3.0', sha256='e63bb32a3e516d8c9bcd149c22335575defdc5896c8bdf15c836608f152a920b')

    depends_on('python@3.5:', type=('build', 'run'), when='@0.7:')
    depends_on('python@3.6:', type=('build', 'run'), when='@0.9:')
    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-pandas@0.23.0:', type=('build', 'run'), when='@0.6:')
    depends_on('py-pandas@0.24.0:', type=('build', 'run'), when='@0.9:')
    depends_on('py-shapely', type=('build', 'run'))
    depends_on('py-shapely@1.6:', type=('build', 'run'), when='@0.9:')
    depends_on('py-fiona', type=('build', 'run'))
    depends_on('py-fiona@1.8:', type=('build', 'run'), when='@0.9:')
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-pyproj@2.2.0:', type=('build', 'run'), when='@0.7:')
