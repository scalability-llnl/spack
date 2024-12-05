# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPy2neo(PythonPackage):
    """Py2neo is a client library and toolkit for working with Neo4j from
    within Python applications and from the command line."""

    homepage = "https://py2neo.org/"
    pypi = "py2neo/py2neo-2.0.8.tar.gz"

    license("Apache-2.0")

    version("4.3.0", sha256="a218ccb4b636e3850faa6b74ebad80f00600217172a57f745cf223d38a219222")
    version("2.0.8", sha256="06167f5a91a0d9b9b73431baacd876f2d507650a681fdce1fcf3b383a9b991c1")
    version("2.0.7", sha256="9b154053eb93c7f5fb3ebd48b6a5b99df450d3f2e9c6682153c6f8d59369378c")
    version("2.0.6", sha256="6bb828d6d3e48b4d095b3f7d79dbb690a47633f0a9812eb62f141b042bab3186")
    version("2.0.5", sha256="2c04d4223d2d356c4800c586f30c048757334f9391553c852c29aebf2368d101")
    version("2.0.4", sha256="727726b87268ca1e929191b960a5473409e5bd81559ee83a304951104bb6b866")

    depends_on("py-setuptools", type="build")
    depends_on("py-certifi", type=("build", "run"), when="@4.3.0:")
    depends_on("py-click@7.0", type=("build", "run"), when="@4.3.0:")
    depends_on("py-colorama", type=("build", "run"), when="@4.3.0:")
    depends_on("py-neobolt@1.7.12:1.7", type=("build", "run"), when="@4.3.0:")
    depends_on("py-neotime@1.7.4:1.7", type=("build", "run"), when="@4.3.0:")
    depends_on("py-prompt-toolkit@2.0.7:2.0", type=("build", "run"), when="@4.3.0:")
    depends_on("py-pygments@2.3.1:2.3", type=("build", "run"), when="@4.3.0:")
    depends_on("py-pytz", type=("build", "run"), when="@4.3.0:")
    depends_on("py-urllib3@1.23:1.24", type=("build", "run"), when="@4.3.0:")
