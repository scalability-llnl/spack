# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAttrs(PythonPackage):
    """Classes Without Boilerplate"""

    homepage = "http://attrs.org/"
    url      = "https://pypi.io/packages/source/a/attrs/attrs-20.3.0.tar.gz"

    version('20.3.0', sha256='832aa3cde19744e49938b91fea06d69ecb9e649c93ba974535d08ad92164f700')
    version('20.2.0', sha256='26b54ddbbb9ee1d34d5d3668dd37d6cf74990ab23c828c2888dccdceee395594')
    version('20.1.0', sha256='0ef97238856430dcf9228e07f316aefc17e8939fc8507e18c6501b761ef1a42a')
    version('19.3.0', sha256='f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72')
    version('19.2.0', sha256='f913492e1663d3c36f502e5e9ba6cd13cf19d7fab50aa13239e420fef95e1396')
    version('19.1.0', sha256='f0b870f674851ecbfbbbd364d6b5cbdff9dcedbc7f3f5e18a6891057f21fe399')
    version('18.1.0', sha256='e0d0eb91441a3b53dab4d9b743eafc1ac44476296a2053b6ca3af0b139faf87b')
    version('16.3.0', sha256='80203177723e36f3bbe15aa8553da6e80d47bfe53647220ccaa9ad7a5e473ccc')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
