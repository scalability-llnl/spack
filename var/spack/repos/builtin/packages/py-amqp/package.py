# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmqp(PythonPackage):
    """Low-level AMQP client for Python (fork of amqplib)."""

    homepage = "https://pypi.org/project/amqp/"
    url      = "https://pypi.io/packages/source/a/amqp/amqp-2.4.1.tar.gz"

    version('5.0.1', sha256='9881f8e6fe23e3db9faa6cfd8c05390213e1d1b95c0162bc50552cad75bffa5f')
    version('2.6.1', sha256='70cdb10628468ff14e57ec2f751c7aa9e48e7e3651cfd62d431213c0c4e58f21')
    version('2.5.2', sha256='77f1aef9410698d20eaeac5b73a87817365f457a507d82edf292e12cbb83b08d')
    version('2.4.2', sha256='043beb485774ca69718a35602089e524f87168268f0d1ae115f28b88d27f92d7')
    version('2.4.1', sha256='6816eed27521293ee03aa9ace300a07215b11fee4e845588a9b863a7ba30addb')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-vine@1.1.3:4.999', when="@2.999", type=('build', 'run'))
    depends_on('py-vine@5.0.0:5.999', when="@5.0.0:5.999", type=('build', 'run'))
