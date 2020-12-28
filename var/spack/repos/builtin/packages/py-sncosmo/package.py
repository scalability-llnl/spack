# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySncosmo(PythonPackage):
    """SNCosmo is a Python library for high-level supernova cosmology
    analysis."""

    homepage = "http://sncosmo.readthedocs.io/"
    url = "https://pypi.io/packages/source/s/sncosmo/sncosmo-1.2.0.tar.gz"

    version('1.2.0', sha256='f3969eec5b25f60c70418dbd64765a2b4735bb53c210c61d0aab68916daea588')

    # Required dependencies
    # py-sncosmo binaries are duplicates of those from py-astropy
    extends('python', ignore=r'bin/.*')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))

    # Recommended dependencies
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-iminuit', type=('build', 'run'))
    depends_on('py-emcee', type=('build', 'run'))
    depends_on('py-nestle', type=('build', 'run'))
