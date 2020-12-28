# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOwslib(PythonPackage):
    """OWSLib is a Python package for client programming with Open Geospatial
    Consortium (OGC) web service (hence OWS) interface standards, and their
    related content models."""

    homepage = "http://http://geopython.github.io/OWSLib/#installation"
    url      = "https://pypi.io/packages/source/O/OWSLib/OWSLib-0.16.0.tar.gz"

    version('0.17.1', sha256='b2e7fd694d3cffcee79317bad492d60c0aa887aea6916517c051c3247b33b5a5')
    version('0.16.0', sha256='ec95a5e93c145a5d84b0074b9ea27570943486552a669151140debf08a100554')

    depends_on('py-setuptools',     type='build')
    depends_on('py-python-dateutil@1.5:',  type=('build', 'run'))
    depends_on('py-pytz',           type=('build', 'run'))
    depends_on('py-requests@1.0:',  type=('build', 'run'))
    depends_on('py-pyproj',           type=('build', 'run'))
