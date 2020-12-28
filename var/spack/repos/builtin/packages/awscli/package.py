##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Awscli(PythonPackage):
    """This package provides a unified command line interface to
       Amazon Web Services"""

    homepage = "https://pypi.org/project/awscli/"
    url      = "https://pypi.io/packages/source/a/awscli/awscli-1.16.308.tar.gz"

    version('1.16.308', sha256='3632fb1db2538128509a7b5e89f2a2c4ea3426bec139944247bddc4d79bf7603')
    version('1.16.179', sha256='6a87114d1325358d000abe22b2103baae7b91f053ff245b9fde33cb0affb5e4f')

    depends_on('py-setuptools', type='build')
    depends_on('py-botocore@1.13.44',  when='@1.16.308', type=('build', 'run'))
    depends_on('py-botocore@1.12.169', when='@1.16.179', type=('build', 'run'))
    depends_on('py-docutils@0.10:0.15', type=('build', 'run'))
    depends_on('py-rsa@3.1.2:3.5.0', type=('build', 'run'))
    depends_on('py-s3transfer@0.2.0:0.2.999', type=('build', 'run'))
    depends_on('py-argparse@1.1:', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:3.13', when='^python@:2.6,3.0:3.3', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:5.2',  when='^python@3.4:',         type=('build', 'run'))
    depends_on('py-colorama@0.2.5:0.3.9', when='^python@:2.6,3.0:3.3', type=('build', 'run'))
    depends_on('py-colorama@0.2.5:0.4.1', when='^python@3.4:',         type=('build', 'run'))
    depends_on('py-nose', type='test')
    depends_on('py-mock@1.3.0:', type='test')
