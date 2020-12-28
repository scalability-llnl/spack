# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    url      = "https://pypi.io/packages/source/v/virtualenv/virtualenv-16.7.6.tar.gz"

    version('16.7.6', sha256='5d370508bf32e522d79096e8cbea3499d47e624ac7e11e9089f9397a0b3318df')
    version('16.4.1', sha256='5a3ecdfbde67a4a3b3111301c4d64a5b71cf862c8c42958d30cf3253df1f29dd')
    version('16.0.0', sha256='ca07b4c0b54e14a91af9f34d0919790b016923d157afda5efdde55c96718f752')
    version('15.1.0', sha256='02f8102c2436bb03b3ee6dede1919d1dac8a427541652e5ec95171ec8adbc93a')
    version('15.0.1', sha256='1a74278b8adb383ce4c7619e33c753b1eb7b58dc1e449601c096ca4b76125f84')
    version('13.0.1', sha256='36c2cfae0f9c6462264bb19c478fc6bab3478cf0575f1027452e975a1ed84dbd')
    version('1.11.6', sha256='3e7a4c151e2ee97f51db0215bfd2a073b04a91e9786df6cb67c916f16abe04f7')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    # not just build-time, requires pkg_resources
    depends_on('py-setuptools@40.6.3:', type=('build', 'run'))
