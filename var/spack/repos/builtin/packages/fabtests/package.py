# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fabtests(AutotoolsPackage):
    """Fabtests provides a set of runtime analysis tools and examples that use
       libfabric."""

    homepage = "http://libfabric.org"
    url = "https://github.com/ofiwg/libfabric/releases/download/v1.9.1/fabtests-1.9.1.tar.bz2"

    version('1.9.1', sha256='6f8ced2c6b3514759a0e177c8b2a19125e4ef0714d4cc0fe0386b33bd6cd5585')
    version('1.9.0', sha256='60cc21db7092334904cbdafd142b2403572976018a22218e7c453195caef366e')
    version('1.8.1', sha256='e9005d8fe73ca3849c872649c29811846bd72a62f897ecab73a08c7a9514f37b')
    # old releases, published in a separate repository
    version('1.6.2', sha256='37405c6202f5b1aa81f8ea211237a2d87937f06254fa3ed44a9b69ac73b234e8')
    version('1.6.1', sha256='d357466b868fdaf1560d89ffac4c4e93a679486f1b4221315644d8d3e21174bf')
    version('1.6.0', sha256='dc3eeccccb005205017f5af60681ede15782ce202a0103450a6d56a7ff515a67')
    version('1.5.3', sha256='3835b3bf86cd00d23df0ddba8bf317e4a195e8d5c3c2baa918b373d548f77f29')
    version('1.5.0', sha256='1dddd446c3f1df346899f9a8636f1b4265de5b863103ae24876e9f0c1e40a69d')
    version('1.4.2', sha256='3b78d0ca1b223ff21b7f5b3627e67e358e3c18b700f86b017e2233fee7e88c2e')

    for v in ['1.4.2', '1.5.0', '1.5.3', '1.6.0', '1.6.1', '1.6.2',
              '1.8.1', '1.9.0', '1.9.1']:
        depends_on('libfabric@{0}'.format(v), when='@{0}'.format(v))

    def url_for_version(self, version):
        if version >= Version('1.8.1'):
            url = "https://github.com/ofiwg/libfabric/releases/download/v{0}/fabtests-{0}.tar.bz2"
        else:
            url = "https://github.com/ofiwg/fabtests/releases/download/v{0}/fabtests-{0}.tar.gz"
        return url.format(version.dotted)
