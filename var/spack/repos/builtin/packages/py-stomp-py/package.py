# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStompPy(PythonPackage):
    """Python client library for accessing messaging servers
    (such as ActiveMQ, Artemis or RabbitMQ) using the STOMP
    protocol (STOMP v1.0, STOMP v1.1 and STOMP v1.2)"""

    homepage = "https://github.com/jasonrbriggs/stomp.py"
    pypi = "stomp.py/stomp.py-8.0.0.tar.gz"

    maintainers("haralmha")

    license("Apache-2.0")

    version("8.0.0", sha256="7085935293bfcc4a112a9830513275b2e0f3b040c5aad5ff8907e78f285b8b57")

    depends_on("python@3.6.3:", type=("build", "run"))
    depends_on("py-poetry@0.12:", type="build")
    depends_on("py-docopt@0.6.2:0", type=("build", "run"))
