# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "http://spark.apache.org"
    url      = "https://pypi.org/packages/source/p/pyspark/pyspark-2.3.0.tar.gz"

    version('2.4.0', 'c9d7b7c5e91b13488b657e364ff392a80b2e374b182138e5ec8702a1822bffdc')
    version('2.3.0', '0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e')

    depends_on('py-setuptools', type='build')
    depends_on('py-py4j@0.10.7', when='@2.3.0:2.4.0', type=('build', 'run'))
