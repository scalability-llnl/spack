# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "http://spark.apache.org"
    url      = "https://pypi.io/packages/source/p/pyspark/pyspark-2.3.0.tar.gz"

    version('2.4.4', sha256='13655eb113b8cf5f3f85b24fd92f86c4668a723723bd68949d028fa0df2cf694')
    version('2.3.0', sha256='0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e')

    depends_on('py-setuptools', type='build')
    depends_on('py-py4j', type=('build', 'run'))
