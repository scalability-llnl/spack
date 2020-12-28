# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pugixml(CMakePackage):
    """Light-weight, simple, and fast XML parser for C++ with XPath support"""

    homepage = "http://pugixml.org/"
    url      = "https://github.com/zeux/pugixml/releases/download/v1.10/pugixml-1.10.tar.gz"

    version('1.11', sha256='26913d3e63b9c07431401cf826df17ed832a20d19333d043991e611d23beaa2c')
    version('1.10', sha256='55f399fbb470942410d348584dc953bcaec926415d3462f471ef350f29b5870a')
    version('1.8.1', sha256='929c4657c207260f8cc28e5b788b7499dffdba60d83d59f55ea33d873d729cd4')

    variant('pic', default=True, description='Build position-independent code')
    variant('shared', default=True, description='Build shared libraries')

    conflicts('+shared', when='~pic')

    def cmake_args(self):
        return [
            self.define('BUILD_SHARED_AND_STATIC_LIBS', False),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('CMAKE_POSITION_INDEPENDENT_CODE', 'pic'),
        ]
