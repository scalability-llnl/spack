# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBoto3(PythonPackage):
    """The AWS SDK for Python."""

    homepage = "https://github.com/boto/boto3"
    pypi = "boto3/boto3-1.10.44.tar.gz"

    version('1.17.27', sha256='fa41987f9f71368013767306d9522b627946a01b4843938a26fb19cc8adb06c0')
    version('1.10.44', sha256='adc0c0269bd65967fd528d7cd826304f381d40d94f2bf2b09f58167e5ac05d86')
    version('1.10.38', sha256='6cdb063b2ae5ac7b93ded6b6b17e3da1325b32232d5ff56e6800018d4786bba6')
    version('1.9.169', sha256='9d8bd0ca309b01265793b7e8d7b88c1df439737d77c8725988f0277bbf58d169')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.20.27:1.20.999',  when='@1.17.27', type=('build', 'run'))
    depends_on('py-botocore@1.13.44:1.13.999',  when='@1.10.44', type=('build', 'run'))
    depends_on('py-botocore@1.13.38:1.13.999',  when='@1.10.38', type=('build', 'run'))
    depends_on('py-botocore@1.12.169:1.12.999', when='@1.9.169', type=('build', 'run'))

    depends_on('py-jmespath@0.7.1:0.999', type=('build', 'run'))

    depends_on('py-s3transfer@0.3.0:0.3.999', when='@1.17.27', type=('build', 'run'))
    depends_on('py-s3transfer@0.2.0:0.2.999', when='@:1.10', type=('build', 'run'))
