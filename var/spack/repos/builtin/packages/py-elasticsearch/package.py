# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyElasticsearch(PythonPackage):
    """Python client for Elasticsearch"""

    homepage = "https://github.com/elastic/elasticsearch-py"
    url = "https://pypi.io/packages/source/e/elasticsearch/elasticsearch-5.2.0.tar.gz"

    version('5.2.0', sha256='45d9f8fbe0878a1b7493afeb20f4f6677a43982776ed1a77d9373e9c5b9de966')
    version('2.3.0', sha256='be3080a2bf32dff0a9f9fcc1c087515a25a357645673a976d25ef77166134d81')

    depends_on('py-setuptools', type='build')
    depends_on('py-urllib3@1.8:1.999', type=('build', 'run'))
    # tests_require
    # depends_on('py-requests@1.0.0:2.9.999', type=('build', 'run'))
    # depends_on('py-nose', type=('build', 'run'))
    # depends_on('py-coverage', type=('build', 'run'))
    # depends_on('py-mock', type=('build', 'run'))
    # depends_on('py-pyyaml', type=('build', 'run'))
    # depends_on('py-nosexcover', type=('build', 'run'))
