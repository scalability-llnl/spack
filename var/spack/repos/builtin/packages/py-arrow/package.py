# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArrow(PythonPackage):
    """Arrow is a Python library that offers a sensible and human-friendly
    approach to creating, manipulating, formatting and converting dates,
    times and timestamps. It implements and updates the datetime type,
    plugging gaps in functionality and providing an intelligent module API
    that supports many common creation scenarios. Simply put, it helps you
    work with dates and times with fewer imports and a lot less code."""

    homepage = "https://arrow.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/a/arrow/arrow-0.16.0.tar.gz"

    version('0.16.0', sha256='92aac856ea5175c804f7ccb96aca4d714d936f1c867ba59d747a8096ec30e90a')
    version('0.14.7', sha256='67f8be7c0cf420424bc62d8d7dc40b44e4bb2f7b515f9cc2954fb36e35797656')
    version('0.14.1', sha256='2d30837085011ef0b90ff75aa0a28f5c7d063e96b7e76b6cbc7e690310256685')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-backports-functools-lru-cache@1.2.1:', type=('build', 'run'), when='^python@2.7:2.8')
    depends_on('py-python-dateutil', type=('build', 'run'))
