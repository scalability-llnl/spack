# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygdal(PythonPackage):
    """
    Virtualenv and setuptools friendly version of standard GDAL python
    bindings.

    This package is for you if you had problems installing GDAL in your
    virtualenv. You can install GDAL into your virtualenv using this package
    but you still need to install GDAL library and its header files on your
    system.
    """

    homepage = "https://github.com/nextgis/pygdal"
    url      = "https://pypi.io/packages/source/p/pygdal/pygdal-3.0.1.5.tar.gz"

    version('3.0.4.6', sha256='8e39b58cd9465bb5f41786a7cf6a62df93334c104db05a5bfb8181a0be276b86')
    version('3.0.1.5', sha256='1222f69fe5e6b632d0d2a42d3acb8fac80fb4577c05e01969d8cd5548192ccaa')
    version('2.4.2.5', sha256='73386683c0b10ab43b6d64257fca2ba812f53ec61b268de8811565fd9ae9bacd')
    version('2.4.1.6', sha256='5d1af98ad09f59e34e3b332cf20630b532b33c7120295aaaabbccebf58a11aa4')
    version('2.4.0.6', sha256='728d11f3ecae0cd3493cd27dab599a0b6184f5504cc172d49400d88ea2b24a9c')
    version('1.11.5.3', sha256='746d13b73a284446a1b604772f869789eabfe6e69dee463f537da27845b29fa7')
    version('1.11.4.3', sha256='99d4b0c94d57ae50592924faaa65cc6a0c0892d83764e9f24ef9270c3a4b111a')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.0.0:', type=('build', 'run'))
    depends_on('gdal@3.0.4', type=('build', 'link', 'run'), when='@3.0.4.6')
    depends_on('gdal@3.0.1', type=('build', 'link', 'run'), when='@3.0.1.5')
    depends_on('gdal@2.4.2', type=('build', 'link', 'run'), when='@2.4.2.5')
    depends_on('gdal@2.4.1', type=('build', 'link', 'run'), when='@2.4.1.6')
    depends_on('gdal@2.4.0', type=('build', 'link', 'run'), when='@2.4.0.6')
    depends_on('gdal@1.11.5', type=('build', 'link', 'run'), when='@1.11.5.3')
    depends_on('gdal@1.11.4', type=('build', 'link', 'run'), when='@1.11.4.3')
