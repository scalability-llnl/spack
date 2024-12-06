# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElasticTransport(PythonPackage):
    """Transport classes and utilities shared among Python Elastic client libraries"""

    homepage = "https://github.com/elastic/elastic-transport-python"
    pypi = "elastic-transport/elastic-transport-8.4.0.tar.gz"

    version("8.4.0", sha256="b9ad708ceb7fcdbc6b30a96f886609a109f042c0b9d9f2e44403b3133ba7ff10")

    depends_on("py-setuptools", type="build")
    depends_on("py-urllib3@1.26.2:1", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))
