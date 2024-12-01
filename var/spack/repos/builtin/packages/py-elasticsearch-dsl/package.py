# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElasticsearchDsl(PythonPackage):
    """Elasticsearch DSL is a high-level library whose aim
    is to help with writing and running queries against Elasticsearch.
    It is built on top of the official low-level client (elasticsearch-py).
    """

    homepage = "https://github.com/elastic/elasticsearch-dsl-py"
    pypi = "elasticsearch-dsl/elasticsearch-dsl-7.4.0.tar.gz"

    license("Apache-2.0")

    version("7.4.0", sha256="c4a7b93882918a413b63bed54018a1685d7410ffd8facbc860ee7fd57f214a6d")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-elasticsearch@7.0.0:7", type=("build", "run"))
