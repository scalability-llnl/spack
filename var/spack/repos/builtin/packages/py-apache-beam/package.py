# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApacheBeam(PythonPackage):
    """Apache Beam is a unified programming model for Batch and Streaming."""

    homepage = "https://github.com/apache/beam"
    url      = "https://pypi.io/packages/source/a/apache-beam/apache-beam-2.24.0.zip"

    version('2.24.0', sha256='55c50b1a964bacc840a5e4cc3b4a42c4ef09d12192d215ba3cad65d4d22e09dd')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pip@7.0.0:', type=('build', 'run'))
    depends_on('py-cython@0.28.1:', type=('build', 'run'))
    depends_on('py-avro@1.8.1:1.10.8', type=('build', 'run'), when='^python@:2.9')
    depends_on('py-avro-python3@1.8.1:1.10.0', type=('build', 'run'), when='^python@3.0:')
    depends_on('py-crcmod@1.7:', type=('build', 'run'))
    depends_on('py-dill@0.3.1:0.3.2', type=('build', 'run'))
    depends_on('py-fastavro@0.21.4:0.24', type=('build', 'run'))
    depends_on('py-funcsigs@1.0.2:2', type=('build', 'run'), when='^python@:2.9')
    depends_on('py-future@0.18.2:1.0.0', type=('build', 'run'))
    depends_on('py-futures@3.2.0:4.0.0', type=('build', 'run'), when='^python@:2.9')
    depends_on('py-grpcio@1.29.0:2', type=('build', 'run'))
    depends_on('py-hdfs@2.1.0:3.0.0', type=('build', 'run'))
    depends_on('py-httplib2@0.8:0.18.0', type=('build', 'run'))
    depends_on('py-mock@1.0.1:3.0.0', type=('build', 'run'))
    depends_on('py-numpy@1.14.3:2', type=('build', 'run'))
    depends_on('py-pymongo@3.8.0:4.0.0', type=('build', 'run'))
    depends_on('py-oauth2client@2.0.1:4', type=('build', 'run'))
    depends_on('py-protobuf@3.12.2:4', type=('build', 'run'))
    depends_on('py-pyarrow@0.15.1:0.18.0', type=('build', 'run'), when='^python@3.0:')
    depends_on('py-pydot@1.2.0:2', type=('build', 'run'))
    depends_on('py-python-dateutil@2.8.0:3', type=('build', 'run'))
    depends_on('py-pytz@2018.3:', type=('build', 'run'))
    depends_on('py-pyvcf@0.6.8:0.7.0', type=('build', 'run'), when='^python@:2.9')
    depends_on('py-requests@2.24.0:3.0.0', type=('build', 'run'))
    depends_on('py-typing@3.7.0:3.8.0', type=('build', 'run'), when='^python@:3.5')
    depends_on('py-typing-extensions@3.7.0:3.8.0', type=('build', 'run'))

    conflicts('+py-avro-python3', when='@1.9.2')
