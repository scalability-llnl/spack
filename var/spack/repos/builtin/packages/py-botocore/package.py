# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBotocore(PythonPackage):
    """Low-level, data-driven core of boto 3."""

    homepage = "https://github.com/boto/botocore"
    pypi = "botocore/botocore-1.13.44.tar.gz"

    version('1.20.27', sha256='4477803f07649f4d80b17d054820e7a09bb2cb0792d0decc2812108bc3759c4a')
    version('1.19.52',  sha256='dc5ec23deadbe9327d3c81d03fddf80805c549059baabd80dea605941fe6a221')
    version('1.13.44',  sha256='a4409008c32a3305b9c469c5cc92edb5b79d6fcbf6f56fe126886b545f0a4f3f')
    version('1.13.38',  sha256='15766a367f39dba9de3c6296aaa7da31030f08a0117fd12685e7df682d8acee2')
    version('1.12.169', sha256='25b44c3253b5ed1c9093efb57ffca440c5099a2d62fa793e8b6c52e72f54b01e')

    depends_on('py-setuptools', type='build')
    depends_on('py-jmespath@0.7.1:0.999', type=('build', 'run'))
    depends_on('py-docutils@0.10:0.15', type=('build', 'run'), when='@:1.17.999')
    depends_on('py-ordereddict@1.1', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-simplejson@3.3.0', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-python-dateutil@2.1:2.999', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:2.6', type=('build', 'run'), when='^python@2.6.0:2.6.999')
    depends_on('py-urllib3@1.20:1.25', type=('build', 'run'), when='@:1.14.11')
    depends_on('py-urllib3@1.20:1.23', type=('build', 'run'), when='@:1.13.999 ^python@2.6.0:2.6.999')
    depends_on('py-urllib3@1.20:1.22', type=('build', 'run'), when='@:1.13.999 ^python@3.3.0:3.3.999')
    depends_on('py-urllib3@1.20:1.25.7', type=('build', 'run'), when='@1.14.12:1.18.999 ^python@3.4.0:3.4.999')
    depends_on('py-urllib3@1.20:1.25.999', type=('build', 'run'), when='@1.14.12:1.18.999')
    depends_on('py-urllib3@1.25.4:1.25.7', type=('build', 'run'), when='@1.19.0: ^python@3.4.0:3.4.999')
    depends_on('py-urllib3@1.25.4:1.25.999', type=('build', 'run'), when='@1.19.0:1.19.15')
    depends_on('py-urllib3@1.25.4:1.26.999', type=('build', 'run'), when='@1.19.16:')
