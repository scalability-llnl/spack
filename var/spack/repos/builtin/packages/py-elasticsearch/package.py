# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyElasticsearch(PythonPackage):
    """Python client for Elasticsearch"""

    homepage = "https://github.com/elastic/elasticsearch-py"
    pypi = "elasticsearch/elasticsearch-5.2.0.tar.gz"

    license("Apache-2.0")

    version("8.6.2", sha256="084458e84caa91e3ad807b68aa82c022e785bead853a3b125641a25e894a1d47")
    version("7.6.0", sha256="d228b2d37ac0865f7631335268172dbdaa426adec1da3ed006dddf05134f89c8")
    version("7.5.1", sha256="2a0ca516378ae9b87ac840e7bb529ec508f3010360dd9feed605dff2a898aff5")
    version("6.4.0", sha256="fb5ab15ee283f104b5a7a5695c7e879cb2927e4eb5aed9c530811590b41259ad")
    version("5.2.0", sha256="45d9f8fbe0878a1b7493afeb20f4f6677a43982776ed1a77d9373e9c5b9de966")
    version("2.3.0", sha256="be3080a2bf32dff0a9f9fcc1c087515a25a357645673a976d25ef77166134d81")

    variant("async", when="@8.6.2:", default=False, description="Include support for asyncio")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.7:3", when="@7.6.0:", type=("build", "run"))
    depends_on("py-urllib3@1.8:1", when="@:5.2.0", type=("build", "run"))
    depends_on("py-urllib3@1.21.1:", when="@6:7", type=("build", "run"))
    depends_on("py-elastic-transport@8.0:8", when="@8.6.2:", type=("build", "run"))
    depends_on("py-aiohttp@3.0:3", when="+async", type=("build", "run"))

    # tests_require
    # depends_on('py-requests@1.0.0:2.9', type=('build', 'run'))
    # depends_on('py-nose', type=('build', 'run'))
    # depends_on('py-coverage', type=('build', 'run'))
    # depends_on('py-mock', type=('build', 'run'))
    # depends_on('py-pyyaml', type=('build', 'run'))
    # depends_on('py-nosexcover', type=('build', 'run'))
