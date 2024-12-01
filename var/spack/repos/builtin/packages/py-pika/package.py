# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPika(PythonPackage):
    """Pika is a RabbitMQ (AMQP 0-9-1) client library for Python."""

    homepage = "https://pika.readthedocs.io/"
    git = "https://github.com/pika/pika.git"
    pypi = "pika/pika-1.3.2.tar.gz"

    license("BSD-3-Clause")

    version("1.3.2", sha256="b2a327ddddf8570b4965b3576ac77091b850262d34ce8c1d8cb4e4146aa4145f")
    version("1.3.1", sha256="beb19ff6dd1547f99a29acc2c6987ebb2ba7c44bf44a3f8e305877c5ef7d2fdc")
    version("1.3.0", sha256="15357ddc47a5c28f0b07d80e93d504cbbf7a1ad5e1cd129ecd27afe76472c529")
    version("1.2.1", sha256="e5fbf3a0a3599f4e114f6e4a7af096f9413a8f24f975c2657ba2fac3c931434f")
    version("1.2.0", sha256="f023d6ac581086b124190cb3dc81dd581a149d216fa4540ac34f9be1e3970b89")
    version("1.1.0", sha256="9fa76ba4b65034b878b2b8de90ff8660a59d925b087c5bb88f8fdbb4b64a1dbf")
    version("1.0.0", sha256="fba41293b35c845bd96cfdd29981f0eeff91f705ac0c3ba361a771c4bfbc3485")
    version("0.13.1", sha256="b0640085f1d6398fd47bb16a17713053e26578192821ea5d928772b8e6a28789")
    version("0.13.0", sha256="5338d829d1edb3e5bcf1523b4a9e32c56dea5a8bda7018825849e35325580484")

    variant("gevent", default=False, description="Build with gevent support")
    variant("tornado", default=False, description="Build with tornado support")
    variant("twisted", default=False, description="Build with twisted support")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.2:", when="@1.3.0:", type="build")
    depends_on("py-gevent", when="+gevent", type=("build", "run"))
    depends_on("py-tornado", when="+tornado", type=("build", "run"))
    depends_on("py-twisted", when="+twisted", type=("build", "run"))
