# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "http://spark.apache.org"
    pypi = "pyspark/pyspark-3.0.1.tar.gz"

    version('3.0.1', sha256='38b485d3634a86c9a2923c39c8f08f003fdd0e0a3d7f07114b2fb4392ce60479')
    version('2.4.4', sha256='13655eb113b8cf5f3f85b24fd92f86c4668a723723bd68949d028fa0df2cf694')
    version('2.3.0', sha256='0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e')

    depends_on('python@2.7:3.7', when='@:2.999', type=('build', 'run'))
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-py4j@0.10.9', when='@3.0.1', type=('build', 'run'))
    depends_on('py-py4j@0.10.7', when='@2.4.4', type=('build', 'run'))
    depends_on('py-py4j@0.10.6', when='@2.3.0', type=('build', 'run'))
