# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCelery(PythonPackage):
    """Celery - Distributed Task Queue."""

    homepage = "https://pypi.org/project/celery/"
    url      = "https://pypi.io/packages/source/c/celery/celery-4.2.1.tar.gz"

    version('5.0.0', sha256='313930fddde703d8e37029a304bf91429cd11aeef63c57de6daca9d958e1f255')
    version('4.4.7', sha256='d220b13a8ed57c78149acf82c006785356071844afe0b27012a4991d44026f9f')
    version('4.3.0', sha256='4c4532aa683f170f40bd76f928b70bc06ff171a959e06e71bf35f2f9d6031ef9')

    variant('redis', default=False, description="Use redis transport")
    variant('sqlalchemy', default=False, description="Use sqlalchemy interface")
    # 'auth',
    # 'cassandra',
    # 'django',
    # 'elasticsearch',
    # 'memcache',
    # 'pymemcache',
    # 'couchbase',
    # 'arangodb',
    # 'eventlet',
    # 'rabbitmq'
    # 'gevent',
    # 'msgpack',
    # 'yaml',
    # 'sqs',
    # 'couchdb',
    # 'riak',
    # 'zookeeper',
    # 'solar',
    # 'azureblockblob',
    # 'librabbitmq',
    # 'pyro',
    # 'slmq',
    # 'tblib',
    # 'consul',
    # 'dynamodb',
    # 'mongodb',
    # 'cosmosdbsql',
    # 's3',

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-redis@3.2.0:', when='+redis', type=('build', 'run'))
    depends_on('py-sqlalchemy', when='+sqlalchemy', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', when="@5.0.0:5.999", type=('build', 'run'))
    depends_on('py-click-didyoumean@:0.0.3', when="@5.0.0:5.999", type=('build', 'run'))
    depends_on('py-click-repl@:0.1.6', when="@5.0.0:5.999", type=('build', 'run'))
    depends_on('py-pytz@2019.3:', type=('build', 'run'))
    depends_on('py-billiard@3.6.3:3.999', type=('build', 'run'))
    depends_on('py-kombu@4.6.11', when="@4.3.0:4.999",  type=('build', 'run'))
    depends_on('py-kombu@5.0.0:', when="@5.0.0:5.999", type=('build', 'run'))
    depends_on('py-vine@1.3.0', when="@4.3.0:4.999", type=('build', 'run'))
    depends_on('py-vine@5.0.0:', when="@5.0.0:5.999", type=('build', 'run'))
