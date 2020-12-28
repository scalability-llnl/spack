# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHypothesis(PythonPackage):
    """A library for property based testing."""

    homepage = "https://github.com/HypothesisWorks/hypothesis-python"
    url      = "https://pypi.io/packages/source/h/hypothesis/hypothesis-4.41.2.tar.gz"

    version('5.3.0',  sha256='c9fdb53fe3bf1f8e7dcca1a7dd6e430862502f088aca2903d141511212e79429')
    version('4.57.1', sha256='3c4369a4b0a1348561048bcda5f1db951a1b8e2a514ea8e8c70d36e656bf6fa0')
    version('4.41.2', sha256='6847df3ffb4aa52798621dd007e6b61dbcf2d76c30ba37dc2699720e2c734b7a')
    version('4.24.3', sha256='fd90a319f409f34a173156ca704d6c0c6c0bb30a2e43dbf26aced2c75569e5d5')
    version('4.7.2',  sha256='87944c6379f77634474b88abbf1e5ed5fe966637cc926131eda5e2af5b54a608')
    version('3.7.0',  sha256='0fea49d08f2d5884f014151a5af6fb48d862f6ad567ffc4a2e84abf2f186c423')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-attrs@19.2.0:', when='@4.38.2:', type=('build', 'run'))
    depends_on('py-attrs@16.0.0:', when='@3.44.22:', type=('build', 'run'))
    depends_on('py-attrs', when='@3.28.0:', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:2')
    depends_on('py-sortedcontainers@2.1.0:2.999.0', type=('build', 'run'), when='@4.57.1:')
