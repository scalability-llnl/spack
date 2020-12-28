# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySentrySdk(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    url = "https://pypi.io/packages/source/s/sentry-sdk/sentry-sdk-0.17.6.tar.gz"

    version('0.17.6', sha256='1a086486ff9da15791f294f6e9915eb3747d161ef64dee2d038a4d0b4a369b24')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.10.0:', type=('build', 'run'))
    depends_on('py-certifi', type=('build', 'run'))
    depends_on('py-flask@0.11:', type=('build', 'run'))
    depends_on('py-bottle@0.12.13:', type=('build', 'run'))
    depends_on('py-falcon@1.4:', type=('build', 'run'))
    depends_on('py-django@1.8:', type=('build', 'run'))
    depends_on('py-sanic@0.8:', type=('build', 'run'))
    depends_on('py-celery@3:', type=('build', 'run'))
    depends_on('py-apache-beam@2.12:', type=('build', 'run'))
    depends_on('py-rq@0.6:', type=('build', 'run'))
    depends_on('py-aiohttp@3.5:', type=('build', 'run'))
    depends_on('py-tornado@5:', type=('build', 'run'))
    depends_on('py-sqlalchemy@1.2:', type=('build', 'run'))
    depends_on('py-pyspark@2.4.4:', type=('build', 'run'))
    depends_on('py-pure-eval', type=('build', 'run'))
    depends_on('py-chalice@1.16.0:', type=('build', 'run'))
