# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCelery(PythonPackage):
    """Celery - Distributed Task Queue."""

    pypi = "celery/celery-5.3.6.tar.gz"

    license("BSD-3-Clause")

    version("5.3.6", sha256="870cc71d737c0200c397290d730344cc991d13a057534353d124c9380267aab9")
    version("5.2.3", sha256="e2cd41667ad97d4f6a2f4672d1c6a6ebada194c619253058b5f23704aaadaa82")
    version("5.0.0", sha256="313930fddde703d8e37029a304bf91429cd11aeef63c57de6daca9d958e1f255")
    version("4.4.7", sha256="d220b13a8ed57c78149acf82c006785356071844afe0b27012a4991d44026f9f")
    version("4.3.0", sha256="4c4532aa683f170f40bd76f928b70bc06ff171a959e06e71bf35f2f9d6031ef9")

    variant("redis", default=False, description="Use redis transport")
    variant("sqlalchemy", default=False, description="Use sqlalchemy interface")
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

    depends_on("python@3.7:", type=("build", "run"), when="@5.2.3:")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools@59.1.1:59.6", type=("build", "run"), when="@5.2.3:5.2.4")

    depends_on("py-redis@3.2.0:", when="+redis", type=("build", "run"))
    depends_on("py-redis@3.4.1:3,4.0.2:", when="@5.2.3:+redis", type=("build", "run"))
    depends_on("py-sqlalchemy", when="+sqlalchemy", type=("build", "run"))

    depends_on("py-click@7.0:7", when="@5.0.0:5.0", type=("build", "run"))
    depends_on("py-click@8.0.3:8", when="@5.2", type=("build", "run"))
    depends_on("py-click@8.1.2:", when="@5.3:", type=("build", "run"))
    depends_on("py-click-didyoumean@0.0.3:", when="@5.0.0:5", type=("build", "run"))
    depends_on("py-click-plugins@1.1.1:", when="@5.0.3:", type=("build", "run"))
    depends_on("py-click-repl@:0.1.6", when="@5.0.0:5.0", type=("build", "run"))
    depends_on("py-click-repl@0.2.0:", when="@5.2.0:", type=("build", "run"))
    depends_on("py-pytz@2019.3:", type=("build", "run"), when="@:5.2")
    depends_on("py-pytz@2021.3:", type=("build", "run"), when="@5.2.3:5.2.99")
    depends_on("py-billiard@3.6.3", type=("build", "run"), when="@:5.0.99")
    depends_on("py-billiard@3.6.4.0:3.99", type=("build", "run"), when="@5.1.0:5.2")
    depends_on("py-billiard@4.2.0:5.0", type=("build", "run"), when="@5.3.0:")
    depends_on("py-kombu@4.6.11", when="@4.3.0:4", type=("build", "run"))
    depends_on("py-kombu@5.0.0:", when="@5.0", type=("build", "run"))
    depends_on("py-kombu@5.1.0:", when="@5.1", type=("build", "run"))
    depends_on("py-kombu@5.2.1", when="@5.2.0", type=("build", "run"))
    depends_on("py-kombu@5.2.2", when="@5.2.1:5.2.2", type=("build", "run"))
    depends_on("py-kombu@5.2.3", when="@5.2.3:5.2.99", type=("build", "run"))
    depends_on("py-kombu@5.3.0", when="@5.3.0", type=("build", "run"))
    depends_on("py-kombu@5.3.1", when="@5.3.1", type=("build", "run"))
    depends_on("py-kombu@5.3.2", when="@5.3.4", type=("build", "run"))
    depends_on("py-kombu@5.3.3", when="@5.3.5", type=("build", "run"))
    depends_on("py-kombu@5.3.4:5.3.5", when="@5.3.6", type=("build", "run"))
    depends_on("py-vine@1.3.0", when="@4.3.0:4", type=("build", "run"))
    depends_on("py-vine@5.0.0:5", when="@5.0.0:5", type=("build", "run"))
